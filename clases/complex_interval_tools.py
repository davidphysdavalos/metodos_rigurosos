import cpintervalo as cpi
import cintervalo as ci
import intervalo as ri


def polar2cart(x):
    
    if not isinstance(x, cpi.CPIntervalo):
        
        print 'Esto no es un intervalo en coordenadas polares'
        
        return None
    
    return ci.CIntervalo(x.mod*cpi.cos(x.arg), x.mod*cpi.sin(x.arg))
    
def cart2polar(x):
    
    if not isinstance(x, ci.CIntervalo):
        
        print 'Esto no es un intervalo en coordenadas cartesianas'
        
        return None
    
    return cpi.CPIntervalo(x.abs(), x.arg())
    
def modulo(x, value):
    
    '''
    Se llama a la libreria Intervalo y se aplica module al argumento del CPIntervalo
    '''
    
    if isinstance(x, ci.CIntervalo):
        
        print 'Este comando funciona solo para CPIntervalo'
        
        return None
    
    if not isinstance(x, cpi.CPIntervalo):
        
        x=cpi.CPIntervalo(x)
        
    xmod= x.mod
    xarg=x.arg
    
    return cpi.CPIntervalo(xmod, ri.module(xarg, value))
    
    
    ##################Metodo de Newton para intervalos####################
    
    
def NewtonOperator(f,fprime,x):
    '''
    NewtonOperator(f,fprime,x), auxiliar en el metodo de Newton para intervalos.
    '''
    m=x.middle()
    
    return m-f(m)/fprime(x)

def intervaliterator(f,fp,x,n):
    
    '''
    iterator(f,fp,x,n), Metodo de Newton para intervalos
    en una dimencion.
    
    '''
    
    a=x
    
    for k in range(0,n):
    
        N=NewtonOperator(f,fp,x)
        
        x=x&N
        
        if x is None:
            
            print 'No convergio a la raiz'
            
            return None
        
        if x==a:
            
            print 'El metodo no va a converger, el operador de Newton hace mas grande el intervalo inicial'
            
            return None
            
        a=x
        
    return x
    
    