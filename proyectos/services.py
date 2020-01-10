from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import os, sys
from pathlib import Path, WindowsPath
import subprocess
from .models import Proyectos, Imagenes, Categorias2

p = 'python'
dirScript = os.path.abspath('proyectos/custom_vision/proyectos')
dirMedia = os.path.abspath('media')
dirModels = os.path.abspath('models')
samples = '--samples'
feat = '--feature-map-file'
codebook = '--codebook-file'
svm = '--svm-file'
inp = '--input-image'
arm = 'Armadillo'
coy = 'Coyote'
tla = 'Tlacuache'
featPKL = 'feature_map.pkl'
codepkl = 'codebook.pkl'
svmpkl = 'svm.pkl'

dirCode = dirModels+('\\'+codepkl)
dirCode = dirCode.replace('\\','/')

dirFeat = dirModels+('\\'+featPKL)
dirFeat = dirFeat.replace('\\','/')

dirSVM = dirModels+('\\'+svmpkl)
dirSVM = dirSVM.replace('\\','/')

def extract_features():
  print('******************Inicio de extración de catacteristicas******************')
  filename = dirScript+('\\'+'create_features.py')
  filename = filename.replace('\\','/')

  dirArm = dirMedia+('\\'+arm)
  dirArm = dirArm.replace('\\','/')
  print(dirArm)

  dirCoy = dirMedia+('\\'+coy)
  dirCoy = dirCoy.replace('\\','/')
  print(dirCoy)

  dirTla = dirMedia+('\\'+tla)
  dirTla = dirTla.replace('\\','/')
  print(dirTla)

  try:
    script = subprocess.run(['python', str(filename),
                              samples, arm, str(dirArm),
                              samples, coy, str(dirCoy), 
                              samples, tla, str(dirTla), 
                              codebook ,str(codepkl) ,
                              feat, str(dirFeat)])
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
  filename = dirScript+('\\'+'training.py')
  filename = filename.replace('\\','/')

  print('F :',dirFeat)
  print('S :',dirSVM)

  try:
    script = subprocess.run([p, str(filename),
                            feat, str(dirFeat), 
                            svm, str(dirSVM)])
    print(script.returncode)
    print(script.stdout)
    print(script.stderr)
    print('******************Entrenamiento listo******************')
  except subprocess.CalledProcessError as identifier:
    print('>>>>>>>>>>>', identifier)
  
  return True

def clasification():
  filename = dirScript+('\\'+'classify_data.py')
  filename = filename.replace('\\','/')

  try:
    for a in Imagenes.objects.all():
      img=str(a.image)
      print(img)
      media = dirMedia.replace('\\','/')
      print('M :',media)
      media = media+('/'+img)
      print('M :',media)
      print('C :',dirCode)

      print('******************Inicio de Clasificación******************')
      script = subprocess.check_output(['python',str(filename),
                              inp,str(media),
                              svm, str(dirSVM), 
                              codebook, str(dirCode)])
      print('****************** fin de Clasificación******************')
      #Guardar en Categorias2
      clasification=Categorias2(tag=script.decode().replace("['",'').replace("']",'') )
      clasification.save()
      a.tag = clasification
      a.save()

    for category in Categorias2.objects.all():
      cat = category.tag
      aa = [cat]
      #print('a = ',aa)
      p = [a.save()]
      #print('p = ',p)
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