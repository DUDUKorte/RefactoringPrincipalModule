import face_recognition
import numpy as np
import time
from debug import *

class FaceRecognitionMethod:
    def __init__(self, detect_params):
        self.model = detect_params['model']
        self.locations_upsample = detect_params['locations_upsample']
        self.encoding_resample = detect_params['face_encoding_resample']
        self.tolerance = detect_params['tolerance']
        self.distance = detect_params['distance_percentage']

    def get_main_face_location(self, frame):
        face_locations = self.get_face_locations(frame)
        maior_area = 0
        main_face_location = None
        i=0

        for face_location in zip(face_locations,):
            i+=1
            face_location = face_location[0]
            top = face_location[0]
            right = face_location[1]            
            bottom = face_location[2]
            left = face_location[3]
            largura = right-left
            altura = bottom - top
            frame_height, frame_width, frame_channels = frame.shape
            area = largura * altura
            plog(f'faces: {i}\naltura: {altura}\nlargura: {largura}\ntop, right, bottom, left: {top, right, bottom, left}\
                \nMaior area: {maior_area}\nArea: {area}\nDistancia mínima: {frame_width*self.distance}\nFrame_largura:{frame_width}\
                \nframe_altura: {frame_height}')
            # Verificar se o rosto está enquadrado na câmera
            if left < 0 or right > frame_width or top < 0 or bottom > frame_height:
                plog(f'PESSOA FORA DO FRAME')
                continue
            # Verficar se o rost está dentro da distância mínima definida
            if largura < frame_width * self.distance:
                plog(f'PESSOA FORA DISTÂNCIA MÍNIMA')
                continue
            # Verifica se a face dentro do quadro é a maior face
            if area > maior_area:
                maior_area = area
                main_face_location = face_location
        
        plog(f'MAIOR ÁREA ENCONTRADA: {maior_area}')



        return main_face_location

    def get_face_locations(self, frame):
        # código reutilizado do sistema anterior
        face_locations = face_recognition.face_locations(frame, self.locations_upsample, self.model)
        #if face_locations:
        return face_locations
    
    def get_encoded_face(self, frame, locations):
        # for face_location in zip(locations):
        #     face_location = [face_location[0]]
        #     print('FACE ENCODED')
        return face_recognition.face_encodings(frame, [locations], self.encoding_resample, 'large')

    def decode_face(self, encoded_faces, face_encoding):
        # fazer o face_distance com self.tolerance
        # retornar o ID da pessoa reconhecida ou None (não reconheceu)
        try:
            face_encoding = face_encoding[0]
        except:
            face_encoding = face_encoding
        names = list(encoded_faces.keys())
        encoded_faces = list(encoded_faces.values())

        face_distances = list(face_recognition.face_distance(encoded_faces, face_encoding))
        plog(face_distances)
        # Pega os menores valores de cada face
        min_distances = list(min(distance) for distance in face_distances) 
        # verificar se a lista são só números ou algoa a mais

        if min(min_distances) <= self.tolerance:
            plog(names[min_distances.index(min(min_distances))]) 

            linha_correta = min_distances.index(min(min_distances)) #TODO:  TESTAR ISSO AQUI
            return encoded_faces[0, linha_correta] # isso deve ser o id que queremos
        else:
            return None
        
    def _decode_face_lists(self, encoded_faces, face_encoding, distance = False):
        try:
            face_encoding = face_encoding[0]
        except:
            face_encoding = face_encoding
        
        ids = encoded_faces[0]
        encoded_faces = encoded_faces[1]
        plog(f'TOTAL FACES TO COMPARE: {len(ids)}')

        comparision_start = time.time()
        if not distance:
            # Abordagem "clássica" que usamos no evento da mostra científica do IF
            results = face_recognition.compare_faces(encoded_faces, face_encoding, tolerance=self.tolerance)
            match = None
            if True in results:
                match = ids[results.index(True)]
                comparision_end = time.time()
                plog(f'COMPARISION TIME : {comparision_end - comparision_start}')
                return match
            else:
                return None
        else:
            # Utilizando o método com face distance
            face_distances = list(face_recognition.face_distance(encoded_faces, face_encoding))
            min_face_distance = min(face_distances)
            if min_face_distance <= self.tolerance:
                match = ids[face_distances.index(min_face_distance)]
                comparision_end = time.time()
                plog(f'COMPARISION TIME : {comparision_end - comparision_start}')
                return match
            else:
                return None