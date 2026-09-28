import tensorflow as tf

def build_cnn(input_dim, learning_rate=.001, filters=(32,64), kernel_size=3, dropout=.3):
    """1D CNN for tabular flow features, treating selected features as an ordered vector."""
    x=tf.keras.Input(shape=(input_dim,),name='flow_features')
    z=tf.keras.layers.Reshape((input_dim,1))(x)
    z=tf.keras.layers.Conv1D(filters[0],kernel_size,padding='same',use_bias=False)(z)
    z=tf.keras.layers.BatchNormalization()(z); z=tf.keras.layers.Activation('relu')(z)
    z=tf.keras.layers.MaxPooling1D(pool_size=2,padding='same')(z)
    z=tf.keras.layers.Conv1D(filters[1],kernel_size,padding='same',use_bias=False)(z)
    z=tf.keras.layers.BatchNormalization()(z); z=tf.keras.layers.Activation('relu')(z)
    z=tf.keras.layers.GlobalAveragePooling1D()(z)
    z=tf.keras.layers.Dense(64,activation='relu')(z); z=tf.keras.layers.Dropout(dropout)(z)
    out=tf.keras.layers.Dense(1,activation='sigmoid',name='attack_probability')(z)
    model=tf.keras.Model(x,out,name='traffic_cnn')
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),loss='binary_crossentropy',metrics=['accuracy'])
    return model
