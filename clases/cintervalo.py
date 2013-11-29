from intervalo import *

from complex_interval_tools import *

class CIntervalo(object):
    '''
    Clase auxiliar en la construccion de intervalos complejos
    '''
    def __init__(self, re, im=None):
        
        '''
        La primera entrada de este objeto es el intervalo correspondiente a la parte real
        y la segunda el intervalo de la parte compleja
        '''
        
        #Si no se da la parte imaginaria el Intervalo se toma como real
        
        if im is None:
            im = Intervalo(0)
            
        if not isinstance(re,Intervalo):
            
            re=Intervalo(re)
            
        if not isinstance(im,Intervalo):
            
            im=Intervalo(im)
        
        
        self.re = re
        self.im = im
        
    def __repr__(self):
        return "CIntervalo [{},{}]".format(self.re,self.im)
    
    def __str__(self):
        return "[{},{}]_c".format(self.re,self.im)

    def _repr_html_(self):
        reprn = "[{}, {}]<sub>c</sub> ".format(self.re, self.im)
        reprn = reprn.replace("inf", r"&infin;")
        return reprn
    
    def _repr_latex_(self):
        return "$[{}, {}]_c$".format(self.re, self.im)
    
    def __mul__(self,otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
        
        return CIntervalo(self.re*otro.re-self.im*otro.im, self.im*otro.re+otro.im* self.re)
    
    def __rmul__(self, otro):
        
        return self*otro
        
    def __radd__(self, otro):
        
        return self + otro
    
    def __add__(self,otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
        
        return CIntervalo(self.re+otro.re,self.im+otro.im)
    
    def abs(self):
        
        '''
        No se define el Absoluto en el sentido de intervalos, sino en el sentido de los numeros complejos
        '''
     
        #return CIntervalo(sqrt(self.re**2+self.im**2))
        
        return sqrt(self.re**2+self.im**2)
        
    
    def __div__(self,otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
        
        denominator=otro.abs()**2
        
        numeradorReal= self.re*otro.re+self.im*otro.im
        
        numeradorcomplex = self.im*otro.re-otro.im*self.re
        
        return CIntervalo(numeradorReal/denominator, numeradorcomplex/denominator)
        
        
    
    def __rdiv__(self,otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
            
        return CIntervalo.__div__(otro, self)
        
    def __eq__(self, otro):
        """
        funcion igualdad para intervalos 
        """
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
            
        if self.re == otro.re:
            
            return self.im == otro.im
            
        return False
        
    def reciprocal(self):
        
        if 0 in self:
            #si el intervalo contiene el cero debe de aparecer un error
            raise ZeroDivisionError
        
        return 1.0/self
        
        
    def __neg__(self):
        
        return CIntervalo(-self.re, -self.im)
        
    def __sub__(self, otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
        
        return CIntervalo(self.re-otro.re, self.im-otro.im)
        
    def __rsub__(self, otro):
        
        return self-otro
        
    def exp(self):
        
        aux=exp(self.re)  
        
        return CIntervalo(aux*cos(self.im), aux*sin(self.im))
        
    def log(self):
        
        return CIntervalo(log(self.abs()), self.arg())
        
    def __pow__(self, otro):
        
        '''
        Esta operacion se realiza en la clase de intervalos en coordenadas polares
        '''
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
        
        newself, otro= cart2polar(self), cart2polar(otro)
        
        result=newself**otro
        
        result=polar2cart(result)
        
        return result
        
        #auxlog=log(self)
        
        #if auxlog.re.lo==-float('inf'):
            
         #   print 'El intervalo contiene alguna potencia del cero'
            
          #  return None
        
        #aux= otro*auxlog
        
        #a=exp(aux)
        
        return a
        
    def __rpow__(self, otro):
        
        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)
            
        return otro**self
        
    def sqrt(self):
        
        return self**(0.5)
        
        
    ##Estas funciones jalan bien... creo ####
        
        
    def __and__(self,otro):
        
        if self.re & otro.re==None:
            
            return None
            
        if self.im & otro.im==None:
            
            return None
        
        return CIntervalo(self.re & otro.re, self.im & otro.im)
        
    def __contains__(self, otro):
        

        if not isinstance(otro, CIntervalo):
            
            otro=CIntervalo(otro)

            
        return otro & self == otro 
    
    
    def conjugate(self):
    
        return CIntervalo(self.re,-self.im)


    def middle(self):
    
        return CIntervalo(self.re.middle(),self.im.middle())
    
    
    ##Funciones en construccion ######
    
    def arg(self):
        
        '''
        Regresa el valor principal del argumento
        '''
        
        if self==0:
            
            print 'indefinido'
            
            return None
            
        return 2.0*arctan(self.im/(self.abs()+self.re))
        
    ### Trigonometric Functions
        
    def sin(self):
        
        return CIntervalo(cosh(self.im)*sin(self.re), cos(self.re)*sinh(self.im))
        
    def cos(self):
        
        return sin(self+math.pi*0.5)
        
    def tan(self):
        
        return sin(self)/cos(self)
        
    # Arcotangente pendiente
        
    #def arctan(self):
        
        
#funciones elementales para intervalos complejos, para que funcionen cosas tipo funcion(a)
def exp(x):
    try:
        return x.exp()
    except:
        return math.exp(x)

def log(x):
    try:
        return x.log()
    except:
        return math.log(x)

def sqrt(x):
    try:
        return x.sqrt()
    except:
        return math.sqrt(x)

#def arctan(x):
 #   try:
  #      return x.arctan()
   # except:
    #    return math.arctan(x)

def cos(x):
    try:
        return x.cos()
    except:
        return math.cos(x)

def sin(x):
    try:
        return x.sin()
    except:
        return math.sin(x)

def tan(x):
    try:
        return x.tan()
    except:
        return math.tan(x)
        
def cosh(x):
    try:
        return x.cosh()
    except:
        return math.cosh(x)

def sinh(x):
    try:
        return x.sinh()
    except:
        return math.sinh(x)

def tanh(x):
    try:
        return x.tanh()
    except:
        return math.tanh(x)
        
def arg(x):
    try:
        return x.arg()
    except:
        return CIntervalo.arg(x)
        
    
    
