from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

import subprocess
from .models import Proyectos, Imagenes, Categorias


def extract_features():
  print('******************Inicio de extración de catacteristicas******************')
  try:
    script = subprocess.run(['python', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/proyectos/custom_vision/proyectos/create_features.py', 
                              '--samples', 'Armadillo', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/media/Armadillo',
                              '--samples', 'Coyote', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/media/Coyote/', 
                              '--samples', 'Tlacuache', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/media/Tlacuache/', 
                              '--codebook-file' ,'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/codebook.pkl' ,
                              '--feature-map-file', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/feature_map.pkl'])
    print('ejecucion del codigo')
    print(script.returncode)
    print(script.stdout)
    print(script.stderr)
    print('******************Extracción lista******************')
  except subprocess.CalledProcessError as identifier:
    print('error', identifier)

  return True


def training():
  print('******************Inicio del entrenamiento******************')
  try:
    script = subprocess.run(['python','C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/proyectos/custom_vision/proyectos/training.py',
                            '--feature-map-file', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/feature_map.pkl', 
                            '--svm-file', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/svm.pkl'])
    print(script.returncode)
    print(script.stdout)
    print(script.stderr)
    print('******************Entrenamiento listo******************')
  except subprocess.CalledProcessError as identifier:
    print('>>>>>>>>>>>', identifier)
  
  return True

def clasification():
  
  try:
    for a in Imagenes.objects.all():
      img=str(a.image)
      print('******************Inicio de Clasificación******************')
      script = subprocess.check_output(['python','C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/proyectos/custom_vision/proyectos/classify_data.py',
                              '--input-image','C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/media/'+img, 
                              '--svm-file', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/svm.pkl', 
                              '--codebook-file', 'C:/Users/ferna/Documents/1Residencias/Pruebas/prueba2/models/codebook.pkl'])
      print('****************** fin de Clasificación******************')
      
      clasification=Categorias(tag=script.decode().replace("['",'').replace("']",'') )
      clasification.save()
      a.tag = clasification
      a.save()
      #return True

    for category in Categorias.objects.all():
      cat = category.tag
      aa = [cat]
      print('a = ',aa)
      p = [a.save()]
      print('p = ',p)
      #r = confusion_matrix(aa, p)
      #print('Confusion matrix: ', r)
      #print('Accuracy Score :',accuracy_score(aa, p))
      #print('***  Report :  ***')
      #print(classification_report(a, p))
  except subprocess.CalledProcessError as identifier:
    print('error', identifier)
  return True

#extract_features()
#training()
#clasification()