import numpy
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import BayesianRidge, Ridge,Lasso,RidgeCV
from sklearn import cross_validation
from sklearn.preprocessing import PolynomialFeatures
from sklearn.kernel_ridge import KernelRidge
from sklearn.feature_selection import RFECV
from sklearn.externals import joblib

def readdata(file):
    X=[]
    y=[]
    "read data from file"
    with open(file) as f:
        data = f.read()
        if len(data)>0:
            data = data.split('\n')
            for i,row in enumerate(data):
                if len(row)>0:
                    data[i]=row.split(",")
                    for j,elem in enumerate(data[i]):
                        if elem=='true':
                            data[i][j]=1.0
                        elif elem=='false':
                            data[i][j]=0.0
                        elif elem=='':
                            data[i].pop(j)
                        else:
                            data[i][j]=float(elem)
                    if data[i][0]!=data[i][1]:
                        X.append(data[i][1:])
                        #XX.append(data[i][1:300])
                        y.append(data[i][0])
        f.close()
    return X,y


X,y=readdata("data.csv")
print X,y
reg=RidgeCV(alphas=[0.0001,0.001,0.01,0.1, 1.0, 10.0],cv=10)
reg.fit(X,y)
ytrain=reg.predict(X)
STD=math.sqrt(np.dot(np.array(ytrain-y),np.array(ytrain-y))/float(len(ytrain)))
Xtest,ytest=readdata("test.csv")

error=0
RMSE=0
if len(ytest)>0:
    ypred=reg.predict(Xtest)
    error=np.dot(np.array(ypred-ytest),np.array(ypred-ytest))
#    print error
#    my=sum(ytest)/float(len(ytest))
#    vv=[(yy-my)*(yy-my) for yy in ytest]
#    print (1-reg.score(Xtest, ytest))*sum(vv)
    RMSE=math.sqrt(error/float(len(ytest)))

#print reg.alpha_
#print reg.intercept_,reg.coef_
param=open("model.csv",'w')
param.write("bias and coefficients,")
param.write(str(reg.intercept_))
for c in reg.coef_:
    param.write(","+str(c))
param.write("\n")
param.write("STD,")
param.write(str(STD))
param.write("\n")
param.write("not normalized squared error,"+ str(error))
param.write("\n")
param.write("RMSE,"+ str(RMSE))
param.write("\n")
param.write(str(type(reg))+",")
param.write(str(reg.alpha_))
param.close()

# save model
#joblib.dump(reg, 'model.pkl')
#clf = joblib.load('model.pkl')


exit()