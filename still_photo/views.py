import collections
import json
import pickle
import urllib.request
import face_recognition
import numpy as np
from django.http import HttpResponse


def homepage(request):
    with open('dataset_faces.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)

    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    face_encodings_only = np.array([face_encoding[0] for face_encoding in face_encodings])
    face_image_path = [all_face_encoding[1] for all_face_encoding in all_face_encodings.values()]
    try:
        url = "https://lh6.googleusercontent.com/-9_mm3Rx85Y8/AAAAAAAAAAI/AAAAAAAABBI/5iJjIJuApWQ/il/photo.jpg"
        resp = urllib.request.urlopen(url)

        unknown_person = face_recognition.load_image_file(resp)
        face_vectors = face_recognition.face_locations(unknown_person)
        if len(face_vectors) > 0:
            unknown_person_encodings = face_recognition.face_encodings(unknown_person)
            confidence_score = face_recognition.face_distance(face_encodings_only, unknown_person_encodings)
            face_recognition.compare_faces(face_encodings_only, unknown_person_encodings, tolerance=0.54)
            name_with_result = dict(zip(face_names, zip((((confidence_score) * -100) + 100), face_image_path)))
            c = collections.Counter(name_with_result)
            result = dict(c.most_common(4))
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse("This is not a face")
    except ValueError as e:
        return HttpResponse("Guy is not registered")
    except OSError as e:
        return HttpResponse("Quality of Image not good enough")
