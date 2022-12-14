from rest_framework.views import APIView
from rest_framework.response import Response
import numpy

#GIVEN_SEATS = 4

def __d_hondt_ratio(votes, seats_taken):
    #Cociente de D'Hondt a ser calculado para cada opción, para cada escaño
    ratio = votes / (seats_taken+1)
    return ratio

def __d_hondt_vote_count(tally, options):
    #Diccionario con una clave por opción, con el número de votos recibidos en los valores
    result = {}
    for option in options:
        result[option["number"]] = 0

    for vote in tally:
        result[vote] += 1
    
    return result

def d_hondt(tally, given_seats, options):

    #Comprobación para evitar bucles infinitos
    if(given_seats <= 0):
        raise ValueError(
            "Invalid number of seats was given. Must be above 0"
        )

    #Diccionario con una clave por opción, con el número de escaños asignados en los valores
    result = {}
    for option in options:
        result[option["number"]] = 0
    
    votes = __d_hondt_vote_count(tally, options)

    #Memoria donde, para cada escaño, calcula el cociente de D'Hondt 
    ratio_dict = {}
    for option in options:
        opt_ratio = __d_hondt_ratio(votes[option["number"]],result[option["number"]])
        ratio_dict[option["number"]] = opt_ratio

    for i in range(given_seats):
        #Calcula la opción con más votos según el cociente de D'Hondt
        max_ratio_index = max(ratio_dict.keys(), key=(lambda key: ratio_dict[key]))
        
        #Añade un escaño a la opción ganadora de esta iteración
        result[max_ratio_index] += 1

        #Actualiza en la memoria únicamente el individuo ganador de esta iteración, excepto si se trata de la última
        if(i < given_seats-1):
            ratio_dict[max_ratio_index] = __d_hondt_ratio(votes[max_ratio_index], result[max_ratio_index])
    
    return result


class PostProcView(APIView):

    #aux y request utilizados en caso de recuento borda y sistema D'Hondt, y para ver el tipo de votacion
    def identity(self, options,aux=False,request=False):
        out = []
        if(request != False and request.data.get("questionType") == "borda"):
            dict_post = {}

            #Rellena el diccionario auxiliar con claves, cada clave es un numero que equivale al numero total de opciones
            for i in range(1,len(aux[0])+1):
                dict_post[i] = 0
            
            #Rellena la puntuacion con el orden de cada una de las opciones
            for array in aux:
                for i, item in enumerate(array):
                    dict_post[item] = dict_post[item] + len(options)-i
            
            #Devuelve en el campo 'postproc' de cada opcion su puntuacion, de cara a otros modulos esto es invisible
            for opt in options:
                out.append({
                    **opt,
                    'postproc': dict_post[opt["number"]],
                });
        elif(request != False and request.data.get("questionType") == "dhondt"):

            votes_dict = d_hondt(aux, request.data.get("seats"), options)

            for opt in options:
                out.append({
                    **opt,
                    'postproc': votes_dict[opt["number"]],
                });
        else:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': opt['votes'],
                });
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        #Debido a que por ejemplo, para una lista con 3 opciones y 2 votantes le entra [1,3,2,3,1,2], hay que separar en [[1,3,2],[3,1,2]]
        if(request.data.get("questionType") == "borda"):
            aux=[]
            tally = request.data.get("extra", [])
            l = numpy.array_split(numpy.array(tally),len(tally)/len(opts))
            for array in l:
                aux.append(list(array))
        elif(request.data.get("questionType") == "dhondt"):
            tally = request.data.get("extra", [])

        if (t == 'IDENTITY' and request.data.get("questionType") == "borda"):
            return self.identity(opts,aux,request)
        elif (t == 'IDENTITY' and request.data.get("questionType") == "dhondt"):
            return self.identity(opts,tally,request)
        elif (t == 'IDENTITY'):
            return self.identity(opts)

        return Response({})
