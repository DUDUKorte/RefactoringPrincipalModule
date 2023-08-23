import face_recognition
import numpy as np

class FaceRecognitionMethod:
    def __init__(self, detect_params):
        self.model = detect_params['model']
        self.locations_upsample = detect_params['locations_upsample']
        self.encoding_resample = detect_params['face_encoding_resample']
        self.tolerance = detect_params['tolerance']
        self.distance = detect_params['distance_pixels']

    def get_face_locations(self, frame):
        # código reutilizado do sistema anterior
        face_locations = face_recognition.face_locations(frame, self.locations_upsample, self.model)
        if face_locations:
            for face_location in zip(face_locations):
                face_location = face_location[0]
                return face_locations if face_location[2] - face_location[0] > self.distance else None # Retornar valores apenas se a pessoa for encontrada e estiver dentro de uma distancia mínima
    
    def get_encoded_face(self, frame, locations):
        for face_location in zip(locations):
            face_location = [face_location[0]]
            print('FACE ENCODED')
            return face_recognition.face_encodings(frame, face_location, self.encoding_resample, 'large')

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
        print(face_distances)
        # Pega os menores valores de cada face
        min_distances = list(min(distance) for distance in face_distances) 
        # verificar se a lista são só números ou algoa a mais

        if min(min_distances) <= self.tolerance:
            print(names[min_distances.index(min(min_distances))]) 

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
        print(f'TOTAL FACES TO COMPARE: {len(ids)}')

        if not distance:
            # Abordagem "clássica" que usamos no evento da mostra científica do IF
            results = face_recognition.compare_faces(encoded_faces, face_encoding, tolerance=0.5)
            match = None
            if True in results:
                match = ids[results.index(True)]
                return match
            else:
                return None
        else:
            # Utilizando o método com face distance
            face_distances = list(face_recognition.face_distance(encoded_faces, face_encoding))
            min_face_distance = min(face_distances)
            if min_face_distance <= self.tolerance:
                match = ids[face_distances.index(min_face_distance)]
                return match
            else:
                return None