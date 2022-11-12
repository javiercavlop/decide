from rest_framework.views import APIView
from rest_framework.response import Response
import numpy


class PostProcView(APIView):

    def identity(self, options,aux=False,request=False):
        out = []
        if(request.data.get("questionType") == "borda"):
            dictPost = {}

            for i in range(1,len(aux[0])+1):
                dictPost[i] = 0
            
            for array in aux:
                for i, item in enumerate(array):
                    dictPost[item] = dictPost[item] + len(options)-i
            
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
        
        if(request.data.get("questionType") == "borda"):
            aux=[]
            tally = request.data.get("extra",[])
            l = numpy.array_split(numpy.array(tally),len(tally)/len(opts))
            for array in l:
                aux.append(list(array))



        if t == 'IDENTITY':
            return self.identity(opts,aux,request)

        return Response({})
