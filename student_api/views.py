
from django.shortcuts import  get_object_or_404

from .models import Student, Path
from .serializers import StudentSerializer ,PathSerializer


from rest_framework.decorators import api_view #fonksiyonları class gibi davranması için import ediyoruz.
from rest_framework.response import Response # verinin JSON objesi olması için import ediyoruz
from rest_framework import status #status kodlarını göstermek için import ediyoruz

from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet


from rest_framework.decorators import action # ViewSetlerde Class' a yeni fonksiyonlar katmak için kullanabiliriz. 


@api_view()  # default GET
def home(requst):
    return Response({'home': 'This is home page...'})


# http methods ----------->
# - GET (DB den veri çağırma, public)
# - POST(DB de değişklik, create, private)
# - PUT (DB DE KAYIT DEĞİŞKLİĞİ, private)
# - delete (dB de kayıt silme)
# - patch (kısmi update)


   #### class Based Views#####

   #APIVIEW YÖNTENİ

class StudentListCreate(APIView):
        #http methodları yazılır.
    def get(self,request):
        students = Student.objects.all() #tüm öğrencileri çağır
        serializer = StudentSerializer(students, many=True)# öğrencileri serializer dan geçir
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data) #dışarıdan gelen veriyi tablo ile karşılaştırır.
        if serializer.is_valid():
            serializer.save()
            data = {"message" : f"Student{serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_404_NOT_FOUND)




class StudentDetail(APIView):

    def get_obj(self, pk):
        return get_object_or_404(Student, pk=pk)

    def get(self, request,pk):
        student= self.get_obj(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_obj(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = self.get_obj(pk)
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)


#çok kullanılmayan yöntem
#Generİc Views
# Bu yöntemde mixins leri kullanıyoruz.

#? Mixins
# - ListModelMixin
#     - list method 
# - CreateModelMixin
#     - create method
# - RetrieveModelMixin
#     - retrieve method # Tek obje için kullanırız.
# - UpdateModelMixin
#     - update method # Tek obje için kullanırız.
# - DestroyModelMixin
#     - destroy method  # Tek obje için kullanırız.

class StudentGAV(mixins.ListModelMixin,mixins.CreateModelMixin, GenericAPIView ): #listeleme ve oluşturma için yazdık.
    queryset=Student.objects.all() # hangi tablo dan beri çekeçeğini bildiririz.
    serializer_class = StudentSerializer # tablonun serializer ını tanıtırız.

    def get(self, request, *args, **kwargs): #bu methodda listeleme yapar.
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs): # bu methodda oluşturma yapar.
        return self.create(request, *args, **kwargs)

# tek bir öğrenci ile ilgili işlemler
class StudentDetailGAV(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#! Concrete Views

class StudentCV(ListCreateAPIView):
    
    queryset = Student.objects.all() # 2 parametre alır. hangi modelden veri çekeliceğini ve hangi  modelin serializerını kullanılacağını belirtiriz.
    serializer_class = StudentSerializer
    
class StudentDetailCV(RetrieveUpdateDestroyAPIView):
    
    queryset = Student.objects.all() # # 2 parametre alır. hangi modelden veri çekeliceğini ve hangi  modelin serializerını kullanılacağını belirtiriz.
    serializer_class = StudentSerializer

#! ViewSets


class StudentMVS(ModelViewSet):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


    #action decorator sadece ModelViewSet ile Kullanılabilir.
    @action(detail=False, methods=["GET"]) #action bize yeni kabiliyetler kazandırır.
    def student_count(self, request): #Student_count bizim endpointimiz olur.
        count = {
            "student-count" : self.queryset.count()
        }
        return Response(count)


class PathMVS(ModelViewSet):

    queryset = Path.objects.all()
    serializer_class = PathSerializer
    
    @action(detail=True) #tek veri çekeçeğimiz zaman True deriz. methods belirtmezsek default olarak GET olur.
    def student_names(self, request, pk=None):
        path = self.get_object()
        students = path.students.all()
        return Response([i.first_name for i in students])