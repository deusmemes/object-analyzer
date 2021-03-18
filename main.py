from tensorflow.keras.models import model_from_json

model = model_from_json(open('../models/ResUNet-seg-model.json').read())
model.load_weights('../models/ResUNet-segModel-weights.hdf5')

pred = model.predict()

