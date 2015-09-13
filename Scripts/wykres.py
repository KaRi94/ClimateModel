import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] = 18
plt.ion()
# linia, = plt.plot([], [],	'ob', ms=10)


# x =	[0]
y = np.arange(-90 + 7.5, 90, 15)
x = np.arange(0, 360, 1)
# for i in range(1, 200) :
#     x=np.random.normal(0,3,y.size)
#     linia.set_xdata( x )
#     linia.set_ydata( y )
#     plt.title("DATA: "+str(i))
#     plt.axis([min(x)-5,max(x)+5,-90,90])
#     plt.draw() # ponowne rysowanie
#     time.sleep(2)
#
# plt.close ()
