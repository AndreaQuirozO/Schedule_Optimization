import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore') 
pd.set_option('display.max_columns', None)

def ObtenerHorario():
    table1 = {'Profesores': {0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I'},
    'Materias': {0: 'k',
    1: 'j',
    2: 'o',
    3: 'r',
    4: 'p',
    5: 'm',
    6: 'n',
    7: 's',
    8: 'q'},
    'Horarios': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9},
    'Salones': {0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i'},
    'Materias que puede dar cada profesor': {0: 'jsk',
    1: 'om',
    2: 'rns',
    3: 'psq',
    4: 'jon',
    5: 'orq',
    6: 'rpk',
    7: 'pjm',
    8: 'jor'},
    'Disponibilidad de horario de cada profesor': {0: 123,
    1: 246,
    2: 345,
    3: 689,
    4: 986,
    5: 135,
    6: 468,
    7: 136,
    8: 367},
    'Costos Profesores': {0: 10,
    1: 20,
    2: 20,
    3: 10,
    4: 20,
    5: 10,
    6: 10,
    7: 20,
    8: 20},
    'Costos Materias': {0: 10, 1: 5, 2: 5, 3: 5, 4: 10, 5: 10, 6: 5, 7: 5, 8: 5},
    'Costos Horarios': {0: 20,
    1: 20,
    2: 20,
    3: 18,
    4: 18,
    5: 18,
    6: 16,
    7: 16,
    8: 16},
    'Costos Salones': {0: 50,
    1: 50,
    2: 40,
    3: 40,
    4: 50,
    5: 50,
    6: 40,
    7: 40,
    8: 50}}

    df1 = pd.DataFrame(table1)
    return df1


def SepararMateriasHorarios(horario):
    materias = horario['Materias que puede dar cada profesor'].apply(lambda x: pd.Series(list(x)))
    horario = horario.join(materias)
    horario.rename(columns = {0:'M1', 1:'M2', 2:'M3'}, inplace = True)

    horario['Disponibilidad de horario de cada profesor'] = horario['Disponibilidad de horario de cada profesor'].astype(str)
    horario['Horarios'] = horario['Horarios'].astype(str)
    disp = horario['Disponibilidad de horario de cada profesor'].apply(lambda x: pd.Series(list(x)))
    horario = horario.join(disp)
    horario.rename(columns = {0:'D1', 1:'D2', 2:'D3'}, inplace = True)

    d = pd.DataFrame(0, index=np.arange(9), columns=['D4', 'D5','D6', 'D7','D8', 'D9'])
    horario = horario.join(d)

    m = pd.DataFrame(np.nan, index=np.arange(9), columns=['M4', 'M5','M6', 'M7','M8', 'M9'])
    horario = horario.join(m)

    horario = horario[['Profesores',
    'Materias',
    'Horarios',
    'Salones',
    'Materias que puede dar cada profesor','M1',
    'M2',
    'M3', 'M4', 'M5','M6', 'M7','M8', 'M9',
    'Disponibilidad de horario de cada profesor','D1',
    'D2',
    'D3', 'D4', 'D5','D6', 'D7','D8', 'D9',
    'Costos Profesores',
    'Costos Materias',
    'Costos Horarios',
    'Costos Salones']]
    return horario

def MatrizAzul(horario):
    pm = pd.DataFrame(np.nan, index=horario['Profesores'], columns=horario['Materias'])
    l = horario['Materias'].tolist()
    n = 0
    for m in l:
        horario.loc[(horario['M1'] != pm.columns[n]) | (horario['M2'] != pm.columns[n]) | (horario['M3'] != pm.columns[n])
                    , m] = 0
        horario.loc[(horario['M1'] == pm.columns[n]) | (horario['M2'] == pm.columns[n]) | (horario['M3'] == pm.columns[n])
                    , m] = 1
        horario[m] = horario[m].astype(int)
        pm[m] = horario[m].to_numpy()
        n += 1
    return pm


def MatrizAmarillaSinCostos(horario):
    ph = pd.DataFrame(np.nan, index=horario['Profesores'], columns=horario['Horarios'])
    l = horario['Horarios'].tolist()
    n = 0
    for m in l:
        horario.loc[(horario['D1'] != ph.columns[n]) | (horario['D2'] != ph.columns[n]) | (horario['D3'] != ph.columns[n])
                    , m] = 0
        horario.loc[(horario['D1'] == ph.columns[n]) | (horario['D2'] == ph.columns[n]) | (horario['D3'] == ph.columns[n])
                    , m] = 1
        horario[m] = horario[m].astype(int)
        ph[m] = horario[m].to_numpy()
        n += 1
    return ph


def MatrizAmarillaCostos(horario, ph):
    cph = ph.append(pd.DataFrame([horario['Costos Horarios'].to_numpy().tolist()],
                             columns=ph.columns.tolist()), ignore_index=True)
    horario2 = horario.copy()
    horario2.loc['Costos Profesores'] = horario2.iloc[:,-2:].sum()
    cph['Costos Profesores'] = horario2['Costos Profesores'].to_numpy().astype(int)
    return cph


def MatrizNaranja(ph, pm, h, mat):
    c = 0
    f = 0
    t = 0
    m = ph.copy()
    for n in h:
        for i in range(len(h)):
            if (pm.iloc[i][mat] == 1 & ph.iloc[i][n] == 1):
                m.iloc[i][n] = ph.iloc[9][n] + ph.iloc[i]['Costos Profesores']
            else:
                m.iloc[i][n] = 0   
    return m


def MatrizVerdeGris(dfmat, hlist, plist):
    df = dfmat[hlist].drop(dfmat.index[len(dfmat)-1])
    minimum = df[df.gt(0)].min(0).min()
    for n in hlist:
      for i in range(len(hlist)):
        if (df.iloc[i][n] == minimum):
          df.iloc[i][n] = 1
        else:
          df.iloc[i][n] = 0
    suma = 0
    for n in hlist:
      for i in range(len(hlist)):
        suma += df.iloc[i][n]
        if(suma > 1):
          df.iloc[i][n] = 0
        df.index = plist
        mat = df.where(df.eq(1)).stack().index.tolist()[0][0]
        hor = df.where(df.eq(1)).stack().index.tolist()[0][1]
    return df, mat, hor, minimum


def Agregar_Prof_Hor(dic, m, mxp, mxh, minimum):
    dic['Materia'].append(m)
    dic['Profesor'].append(mxp)
    dic['Horario'].append(mxh)
    dic['Costos Profesor Horario'].append(minimum)


def RestaMatrizGrizAmarilla(ph, mat):
    nph = ph.subtract(mat, axis = 1)
    return nph


def GenerarMatrices(materiaslist, horarioslist, profesoreslist, horario, pm, ph, dic):
    for n in materiaslist:
        cph = MatrizAmarillaCostos(horario, ph)
        mn = MatrizNaranja(cph, pm, horarioslist, n)
        mnmat, mnp, mnh, minimum = MatrizVerdeGris(mn, horarioslist, profesoreslist)
        Agregar_Prof_Hor(dic, n, mnp, mnh, minimum)
        ph =  RestaMatrizGrizAmarilla(ph, mnmat)
    return ph


def CrearTablaAzul(dic):
    tabazul = pd.DataFrame(dic)
    return tabazul


def CostosSalones(horario, horarioslist):
    salones = horario[['Salones', 'Costos Salones']].sort_values('Costos Salones')

    sal = pd.DataFrame("", index = [0], columns=horarioslist)
    sal = pd.DataFrame("", index = [0], columns=horarioslist)
    hor = ''.join(salones['Salones'].tolist())
    for n in range(0,9):
        sal.iloc[0][n] = hor[:n+1]

    cossal = pd.DataFrame(np.nan, index = [0], columns=horarioslist)
    cos = salones['Costos Salones'].to_list()
    c = 0
    for n in range(0,9):
        c += cos[n]
        cossal.iloc[0][n] = c
    return sal, cossal

def CreartablaVerde(horario):
    tabverde = horario[['Horarios', 'Materias', 'Costos Materias']]
    tabverde.insert(1,"Salones a utilizar", "")
    tabverde.insert(2,"Costos Salones", "")
    return tabverde

def CalcularCostosSalon(tabazul, tabverde, horarioslist, sal, cossal):
    for r in horarioslist:
        if (len(tabazul.loc[(tabazul['Horario'] == r)])) == 0:
            tabverde.loc[tabverde['Horarios'] == r, 'Salones a utilizar'] = 'Ninguno'
            tabverde.loc[tabverde['Horarios'] == r, 'Costos Salones'] = 0
        else:
            tabverde.loc[tabverde['Horarios'] == r, 
                         'Salones a utilizar'] = sal.iloc[0][len(tabazul.loc[(tabazul['Horario'] == r)])-1]
            tabverde.loc[tabverde['Horarios'] == r, 
                         'Costos Salones'] = cossal.iloc[0][len(tabazul.loc[(tabazul['Horario'] == r)])-1]
            
    tabverde = tabverde.join(tabazul['Costos Profesor Horario'])
    return tabverde


def CalcularCostoTotal(tabverde):
    total = tabverde[['Costos Salones', 'Costos Materias', 
                    'Costos Profesor Horario']].sum(axis=0).sum()*1000
    return total


def CrearTablaFinal(tabazul, tabverde):
    tabfinal = tabazul
    tabfinal['Salones a utilizar'] = tabverde['Salones a utilizar']
    tabfinal['Costos materia'] = tabverde['Costos Materias']
    tabfinal['Costos salones'] = tabverde['Costos Salones']
    tabfinal = tabfinal[['Horario', 'Salones a utilizar', 
                        'Costos salones', 'Materia', 'Costos materia', 
                        'Profesor', 'Costos Profesor Horario']]
    return tabfinal
    

def HacerTodo(horario):
    horario = SepararMateriasHorarios(horario)
    pm = MatrizAzul(horario)
    ph = MatrizAmarillaSinCostos(horario)

    materiaslist = horario['Materias'].tolist()
    horarioslist = horario['Horarios'].tolist()
    profesoreslist = horario['Profesores'].to_list()
    dic = {'Materia': [], 'Profesor': [], 'Horario': [], 'Costos Profesor Horario': []}

    ph = GenerarMatrices(materiaslist, horarioslist, profesoreslist, horario, pm, ph, dic)
    tabazul = CrearTablaAzul(dic)
    sal, cossal = CostosSalones(horario, horarioslist)
    tabverde = CreartablaVerde(horario)
    tabverde = CalcularCostosSalon(tabazul, tabverde, horarioslist, sal, cossal)
    total = CalcularCostoTotal(tabverde)
    tabfinal = CrearTablaFinal(tabazul, tabverde)

    return tabfinal, total

st.set_page_config(
    page_title='Horario Óptimo',
    layout='wide',
)

st.title("Calculadora para optimizar horarios")

st.markdown("Esta calculadora sirve para optimizar horarios.")


st.header("Restricciones")
horario = ObtenerHorario()
st.write(horario)

st.header("Horario óptimo")
tabfinal, total = HacerTodo(horario)
st.write(tabfinal)
st.markdown(f"El cósto de este horario es: {total:,} unidades.")
print(total)

