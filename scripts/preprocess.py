from src.data.preprocessing import prepare_dataset
if __name__=='__main__':
    X,y,Xt,yt=prepare_dataset(); print(f'Preprocessed: train={X.shape}, test={Xt.shape}, positive_train={int(y.sum())}')
