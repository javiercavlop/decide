from rest_framework.views import APIView
from rest_framework.response import Response
import numpy


class PostProcView(APIView):

    #aux y request utilizados en caso de recuento borda, y para ver el tipo de votacion
    def identity(self, options,aux=False,request=False):
        out = []
        if(request != False and request.data.get("questionType") == "borda"):
            dictPost = {}

            #Rellena el diccionario auxiliar con claves, cada clave es un numero que equivale al numero total de opciones
            for i in range(1,len(aux[0])+1):
                dictPost[i] = 0
            
            #Rellena la puntuacion con el orden de cada una de las opciones
            for array in aux:
                for i, item in enumerate(array):
                    dictPost[item] = dictPost[item] + len(options)-i
            
            #Devuelve en el campo 'postproc' de cada opcion su puntuacion, de cara a otros modulos esto es invisible
            for opt in options:
                out.append({
                    **opt,
                    'postproc': dictPost[opt["number"]],
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
            tally = request.data.get("extra",[])
            l = numpy.array_split(numpy.array(tally),len(tally)/len(opts))
            for array in l:
                aux.append(list(array))

        if (t == 'IDENTITY' and request.data.get("questionType") == "borda"):
            return self.identity(opts,aux,request)
        elif (t == 'IDENTITY'):
            return self.identity(opts)

        return Response({})
