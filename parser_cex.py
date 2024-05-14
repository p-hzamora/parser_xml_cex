from pathlib import Path
from typing import Any, Generator
from lxml import etree
from datetime import datetime

from abc import abstractmethod, ABC

import pandas as pd


def get_value(element: etree._Element):
    if element is not None:
        _element: str = element.text
        # A veces el texto del elemento puedo ser None
        if _element:
            _element = _element.strip()
            try:
                _element = float(_element)
            except ValueError:
                pass
            return _element
    return None


class _Primitive(ABC):
    """
    Clase utilizada para realizar busquedas en un elemento etree._Element
    Tambien se utiliza para aquellas clases que implementen __slots__
    """

    def __init__(self, root: etree._Element):
        if root is None:
            raise Exception(f"el argumento 'root' es {type(root)}.\nSe esperaba {etree._Element}")

        self._root = root

    def __repr__(self):
        return f"< {self.__class__.__name__} >"

    def _find(self, name: str) -> etree._Element:
        return self._root.find(name)

    def set_args(self):
        """
        funcion utilizada para agregar un valor a las variables que estan en __slots__. Lo unico que queremos hacer es quitar el "_" que tienen todas las variables de __slots__.
        Si no pusieramos "_" en las variables __slots__, obtendriamos un error de ambigüedad con las Properties de la clase, por llamarse igual

        """
        for attr in self.__slots__:
            setattr(self, attr, attr.removeprefix("_"))


class _Parser_escala_global(_Primitive):
    """
    Devuelve los valores de la calificacion a escala global

        <EscalaCalefaccion>
            <A>11.70</A>
            <B>27.00</B>
            <C>48.70</C>
            <D>81.60</D>
            <E>144.10</E>
            <F>157.10</F>
        </EscalaCalefaccion>

                o

      <EscalaRefrigeracion>
        <A>5.50</A>
        <B>8.90</B>
        <C>13.90</C>
        <D>21.30</D>
        <E>26.30</E>
        <F>32.40</F>
      </EscalaRefrigeracion>

    """

    __slots__ = ("_A", "_B", "_C", "_D", "_E", "_F")

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def A(self):
        return get_value(self._find(self._A))

    @property
    def B(self):
        return get_value(self._find(self._B))

    @property
    def C(self):
        return get_value(self._find(self._C))

    @property
    def D(self):
        return get_value(self._find(self._D))

    @property
    def E(self):
        return get_value(self._find(self._E))

    @property
    def F(self):
        return get_value(self._find(self._F))


class _Parser_calificacion_instalaciones(_Primitive):
    """
    Clase que devuelve los valores alfabeticos de la calificacion de las instalaciones

        <Calefaccion> E </Calefaccion>
        <Refrigeracion> B </Refrigeracion>
        <ACS> B </ACS>
        <Global> B </Global>
        ...

    """

    __slots__ = ("_Calefaccion", "_Refrigeracion", "_ACS", "_Global")

    def __init__(self, root: etree._Element):
        super().__init__(root)
        self.set_args()

    @property
    def Calefaccion(self):
        return get_value(self._find(self._Calefaccion))

    @property
    def Refrigeracion(self):
        return get_value(self._find(self._Refrigeracion))

    @property
    def ACS(self):
        return get_value(self._find(self._ACS))

    @property
    def Global(self):
        return get_value(self._find(self._Global))


class _Parser_calificacion_EnergiaPrimariaNoRenovable(_Parser_calificacion_instalaciones):
    def __init__(self, root: etree._Element):
        super().__init__(root)
        self._EscalaGlobal = self._root.find("EscalaGlobal")

    @property
    def EscalaGlobal(self):
        return _Parser_escala_global(self._EscalaGlobal)


class _Parser_calificacion_EmisionesCO2(_Parser_calificacion_EnergiaPrimariaNoRenovable):
    """
    Misma clase que _Parser_calificacion_EnergiaPrimariaNoRenovable
    """

    pass


class _Parser_calificacion_demanda(_Parser_calificacion_instalaciones):
    def __init__(self, root: etree._Element):
        super().__init__(root)
        self._EscalaCalefaccion = self._root.find("EscalaCalefaccion")
        self._EscalaRefrigeracion = self._root.find("EscalaRefrigeracion")

    @property
    def EscalaCalefaccion(self):
        return _Parser_escala_global(self._EscalaCalefaccion)

    @property
    def EscalaRefrigeracion(self):
        return _Parser_escala_global(self._EscalaRefrigeracion)


class _Parser_instalaciones(_Primitive):
    __slots__ = ("_ACS", "_Calefaccion", "_Global", "_Refrigeracion", "_Iluminacion", "_GlobalDiferenciaSituacionInicial", "_Conjunta")

    def __init__(self, root: etree._Element):
        super().__init__(root)
        self.set_args()

    @property
    def ACS(self):
        return get_value(self._find(self._ACS))

    @property
    def Calefaccion(self):
        return get_value(self._find(self._Calefaccion))

    @property
    def Global(self):
        return get_value(self._find(self._Global))

    @property
    def Refrigeracion(self):
        return get_value(self._find(self._Refrigeracion))

    @property
    def Iluminacion(self):
        return get_value(self._find(self._Iluminacion))

    @property
    def GlobalDiferenciaSituacionInicial(self):
        return get_value(self._find(self._GlobalDiferenciaSituacionInicial))

    @property
    def Conjunta(self):
        return get_value(self._find(self._Conjunta))


class _Parser_IdentificacionEdificio(_Primitive):
    __slots__ = (
        "_ReferenciaCatastral",
        "_Provincia",
        "_ComunidadAutonoma",
        "_ZonaClimatica",
        "_TipoDeEdificio",
        "_NormativaVigente",
        "_Direccion",
        "_NombreDelEdificio",
        "_Procedimiento",
        "_CodigoPostal",
        "_AlcanceInformacionXML",
        "_Municipio",
        "_AnoConstruccion",
    )

    def __init__(self, root: etree._Element):
        super().__init__(root.find("IdentificacionEdificio"))
        self.set_args()

    @property
    def ReferenciaCatastral(self):
        return get_value(self._find(self._ReferenciaCatastral))

    @property
    def Provincia(self):
        return get_value(self._find(self._Provincia))

    @property
    def ComunidadAutonoma(self):
        return get_value(self._find(self._ComunidadAutonoma))

    @property
    def ZonaClimatica(self):
        return get_value(self._find(self._ZonaClimatica))

    @property
    def TipoDeEdificio(self):
        return get_value(self._find(self._TipoDeEdificio))

    @property
    def NormativaVigente(self):
        norma = get_value(self._find(self._NormativaVigente))
        # Condicion para que devuelva un mensaje mas especifico
        if norma == "Anterior":
            return "Anterior a la NBE-CT-79"
        return get_value(self._find(self._NormativaVigente))

    @property
    def Direccion(self):
        return get_value(self._find(self._Direccion))

    @property
    def NombreDelEdificio(self):
        return get_value(self._find(self._NombreDelEdificio))

    @property
    def Procedimiento(self):
        return get_value(self._find(self._Procedimiento))

    @property
    def CodigoPostal(self):
        return self._find(self._CodigoPostal).text

    @property
    def AlcanceInformacionXML(self):
        return get_value(self._find(self._AlcanceInformacionXML))

    @property
    def Municipio(self):
        return get_value(self._find(self._Municipio))

    @property
    def AnoConstruccion(self):
        return self._find(self._AnoConstruccion).text


class _Parser_DatosDelCertificador(_Primitive):
    __slots__ = (
        "_NIFEntidad",
        "_ComunidadAutonoma",
        "_Titulacion",
        "_Fecha",
        "_NIF",
        "_NombreyApellidos",
        "_RazonSocial",
        "_Municipio",
        "_CodigoPostal",
        "_Provincia",
        "_Telefono",
        "_Email",
        "_Domicilio",
    )

    def __init__(self, root: etree._Element):
        super().__init__(root.find("DatosDelCertificador"))
        self.set_args()

    @property
    def NIFEntidad(self):
        return get_value(self._find(self._NIFEntidad))

    @property
    def ComunidadAutonoma(self):
        return get_value(self._find(self._ComunidadAutonoma))

    @property
    def Titulacion(self):
        return get_value(self._find(self._Titulacion))

    @property
    def Fecha(self):
        return get_value(self._find(self._Fecha))

    @property
    def NIF(self):
        return get_value(self._find(self._NIF))

    @property
    def NombreyApellidos(self):
        return get_value(self._find(self._NombreyApellidos))

    @property
    def RazonSocial(self):
        return get_value(self._find(self._RazonSocial))

    @property
    def Municipio(self):
        return get_value(self._find(self._Municipio))

    @property
    def CodigoPostal(self):
        return self._find(self._CodigoPostal).text

    @property
    def Provincia(self):
        return get_value(self._find(self._Provincia))

    @property
    def Telefono(self):
        return self._find(self._Telefono).text

    @property
    def Email(self):
        return get_value(self._find(self._Email))

    @property
    def Domicilio(self):
        return get_value(self._find(self._Domicilio))


class _Parser_PorcentajeSuperficieAcristalada(_Primitive):
    __slots__ = ("_E", "_NO", "_NE", "_O", "_N", "_S", "_SO", "_SE")

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def E(self):
        return get_value(self._find(self._E))

    @property
    def NO(self):
        return get_value(self._find(self._NO))

    @property
    def NE(self):
        return get_value(self._find(self._NE))

    @property
    def O(self):
        return get_value(self._find(self._O))

    @property
    def N(self):
        return get_value(self._find(self._N))

    @property
    def S(self):
        return get_value(self._find(self._S))

    @property
    def SO(self):
        return get_value(self._find(self._SO))

    @property
    def SE(self):
        return get_value(self._find(self._SE))


class _Parser_DatosGeneralesyGeometria(_Primitive):
    __slots__ = (
        "_VentilacionUsoResidencial",
        "_NumeroDePlantasSobreRasante",
        "_PorcentajeSuperficieHabitableCalefactada",
        "_SuperficieHabitable",
        "_DensidadFuentesInternas",
        "_Compacidad",
        "_VolumenEspacioHabitable",
        "_VentilacionTotal",
        "_DemandaDiariaACS",
        "_Plano",
        "_NumeroDePlantasBajoRasante",
        "_PorcentajeSuperficieHabitableRefrigerada",
        "_Imagen",
        "_PorcentajeSuperficieAcristalada",
    )

    def __init__(self, root: etree._Element):
        self._root = root.find("DatosGeneralesyGeometria")
        self.set_args()

    @property
    def VentilacionUsoResidencial(self):
        return get_value(self._find(self._VentilacionUsoResidencial))

    @property
    def NumeroDePlantasSobreRasante(self):
        return get_value(self._find(self._NumeroDePlantasSobreRasante))

    @property
    def PorcentajeSuperficieHabitableCalefactada(self):
        return get_value(self._find(self._PorcentajeSuperficieHabitableCalefactada))

    @property
    def SuperficieHabitable(self):
        return get_value(self._find(self._SuperficieHabitable))

    @property
    def DensidadFuentesInternas(self):
        return get_value(self._find(self._DensidadFuentesInternas))

    @property
    def Compacidad(self):
        return get_value(self._find(self._Compacidad))

    @property
    def VolumenEspacioHabitable(self):
        return get_value(self._find(self._VolumenEspacioHabitable))

    @property
    def VentilacionTotal(self):
        return get_value(self._find(self._VentilacionTotal))

    @property
    def DemandaDiariaACS(self):
        return get_value(self._find(self._DemandaDiariaACS))

    @property
    def Plano(self):
        return get_value(self._find(self._Plano))

    @property
    def NumeroDePlantasBajoRasante(self):
        return get_value(self._find(self._NumeroDePlantasBajoRasante))

    @property
    def PorcentajeSuperficieHabitableRefrigerada(self):
        return get_value(self._find(self._PorcentajeSuperficieHabitableRefrigerada))

    @property
    def Imagen(self):
        return get_value(self._find(self._Imagen))

    @property
    def PorcentajeSuperficieAcristalada(self):
        return _Parser_PorcentajeSuperficieAcristalada(self._find(self._PorcentajeSuperficieAcristalada))


class IElementContainer(ABC):
    __slots__ = ("_elementos", "_df", "_root")

    def __repr__(self):
        return f"< {self.__class__.__name__} >"

    @property
    def df(self) -> pd.DataFrame:
        return self._create_df()

    @abstractmethod
    def _get_elementos(): ...

    @property
    @abstractmethod
    def elementos(self): ...

    def _create_df(self) -> pd.DataFrame:
        lista = [x.get_dict() for x in self._elementos]
        return pd.DataFrame(lista)


class _CommonAttributes(_Primitive):
    __slots__ = (
        "_Nombre",
        "_Tipo",
        "_Transmitancia",
    )

    def __repr__(self):
        return f"Element <{self.__class__.__name__}>"

    def get_dict(self) -> dict:
        dicc = dict()
        for key in self.__slots__:
            attr = getattr(self, key)
            dicc[attr] = getattr(self, attr)
        return dicc


class _Parser_elemento_CerramientosOpacos(_CommonAttributes):
    __slots__ = _CommonAttributes.__slots__ + (
        "_Superficie",
        "_ModoDeObtencion",
        "_Orientacion",
    )

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def Tipo(self):
        return get_value(self._find(self._Tipo))

    @property
    def ModoDeObtencion(self):
        return get_value(self._find(self._ModoDeObtencion))

    @property
    def Transmitancia(self):
        return get_value(self._find(self._Transmitancia))

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def Orientacion(self):
        return get_value(self._find(self._Orientacion))

    @property
    def Superficie(self):
        return get_value(self._find(self._Superficie))


class _Parser_CerramientosOpacos(IElementContainer):
    def __init__(self, root: etree._Element) -> None:
        self._root: etree._Element = root.find("CerramientosOpacos")
        self._elementos = self._get_elementos()

    def __repr__(self):
        return super().__repr__()

    def _get_elementos(self) -> Generator[_Parser_elemento_CerramientosOpacos, None, None]:
        for elemento in self._root.findall("Elemento"):
            yield _Parser_elemento_CerramientosOpacos(elemento)

    @property
    def elementos(self) -> list[_Parser_elemento_CerramientosOpacos]:
        return [x for x in self._elementos]


class _Parser_elemento_HuecosyLucernarios(_CommonAttributes):
    __slots__ = _CommonAttributes.__slots__ + ("_Superficie", "_ModoDeObtencionTransmitancia", "_Orientacion", "_ModoDeObtencionFactorSolar", "_FactorSolar")

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def Tipo(self):
        return get_value(self._find(self._Tipo))

    @property
    def Superficie(self):
        return get_value(self._find(self._Superficie))

    @property
    def Transmitancia(self):
        return get_value(self._find(self._Transmitancia))

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def ModoDeObtencionTransmitancia(self):
        return get_value(self._find(self._ModoDeObtencionTransmitancia))

    @property
    def Orientacion(self):
        return get_value(self._find(self._Orientacion))

    @property
    def ModoDeObtencionFactorSolar(self):
        return get_value(self._find(self._ModoDeObtencionFactorSolar))

    @property
    def FactorSolar(self):
        return get_value(self._root.find(self._FactorSolar))


class _Parser_HuecosyLucernarios(IElementContainer):
    def __init__(self, root: etree._Element) -> None:
        self._root = root.find("HuecosyLucernarios")
        self._elementos = self._get_elementos()

    def __repr__(self):
        return super().__repr__()

    def _get_elementos(self) -> Generator[_Parser_elemento_HuecosyLucernarios, None, None]:
        for elemento in self._root.findall("Elemento"):
            yield _Parser_elemento_HuecosyLucernarios(elemento)

    @property
    def elementos(self) -> list[_Parser_elemento_HuecosyLucernarios]:
        return [x for x in self._elementos]


class _Parser_elemento_PuentesTermicos(_CommonAttributes):
    __slots__ = _CommonAttributes.__slots__ + ("_ModoDeObtencion", "_Longitud")

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def ModoDeObtencion(self):
        return get_value(self._find(self._ModoDeObtencion))

    @property
    def Transmitancia(self):
        return get_value(self._find(self._Transmitancia))

    @property
    def Tipo(self):
        return get_value(self._find(self._Tipo))

    @property
    def Longitud(self):
        return get_value(self._find(self._Longitud))


class _Parser_PuentesTermicos(IElementContainer):
    def __init__(self, root: etree._Element) -> None:
        self._root = root.find("PuentesTermicos")
        self._elementos = self._get_elementos()

    def __repr__(self):
        return super().__repr__()

    def _get_elementos(self) -> Generator[etree._Element,None, None]:
        for elemento in self._root.findall("Elemento"):
            yield _Parser_elemento_PuentesTermicos(elemento)

    @property
    def elementos(self) -> list[_Parser_elemento_PuentesTermicos]:
        return [x for x in self._elementos]


class _Parser_DatosEnvolventeTermica(_Primitive):
    def __init__(self, root: etree._Element):
        super().__init__(root.find("DatosEnvolventeTermica"))

        self._CerramientosOpacos = _Parser_CerramientosOpacos
        self._HuecosyLucernarios = _Parser_HuecosyLucernarios
        self._PuentesTermicos = _Parser_PuentesTermicos

    @property
    def CerramientosOpacos(self):
        return self._CerramientosOpacos(self._root)

    @property
    def HuecosyLucernarios(self):
        return self._HuecosyLucernarios(self._root)

    @property
    def PuentesTermicos(self):
        return self._PuentesTermicos(self._root)


class _Parser_InstalacionesTermicas_data(_Primitive):
    __slots__ = ("_RendimientoNominal", "_Tipo", "_ModoDeObtencion", "_VectorEnergetico", "_PotenciaNominal", "_Nombre", "_RendimientoEstacional")

    def __init__(self, root: etree._Element) -> None:
        super().__init__(root)
        self.set_args()

    @property
    def RendimientoNominal(self):
        return get_value(self._find(self._RendimientoNominal))

    @property
    def Tipo(self):
        return get_value(self._find(self._Tipo))

    @property
    def ModoDeObtencion(self):
        return get_value(self._find(self._ModoDeObtencion))

    @property
    def VectorEnergetico(self):
        return get_value(self._find(self._VectorEnergetico))

    @property
    def PotenciaNominal(self):
        return get_value(self._find(self._PotenciaNominal))

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def RendimientoEstacional(self):
        return get_value(self._find(self._RendimientoEstacional))


class _Parser_InstalacionesTermicas(object):
    def __init__(self, root: etree._Element):
        self._root = root.find("InstalacionesTermicas")

    @property
    def GeneradoresDeCalefaccion(self):
        return _Parser_InstalacionesTermicas_data(self._root.find("GeneradoresDeCalefaccion").find("Generador"))

    @property
    def InstalacionesACS(self):
        return _Parser_InstalacionesTermicas_data(self._root.find("InstalacionesACS").find("Instalacion"))


class _Parser_CondicionesFuncionamientoyOcupacion(_Primitive):
    __slots__ = ("_Nombre", "_Superficie", "_NivelDeAcondicionamiento", "_PerfilDeUso")

    def __init__(self, root: etree._Element):
        self.set_args()
        self._root = root.find("CondicionesFuncionamientoyOcupacion").find("Espacio")

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def Superficie(self):
        return get_value(self._find(self._Superficie))

    @property
    def NivelDeAcondicionamiento(self):
        return get_value(self._find(self._NivelDeAcondicionamiento))

    @property
    def PerfilDeUso(self):
        return get_value(self._find(self._PerfilDeUso))


class _Parser_Demanda(object):
    def __init__(self, root: etree._Element):
        self._root = root.find("Demanda")

        self.EdificioObjeto = _Parser_instalaciones(self._root.find("EdificioObjeto"))


class _Parser_combustibles(_Primitive):
    __slots__ = (
        "_GasNatural",
        "_ElectricidadBaleares",
        "_BiomasaOtros",
        "_ElectricidadCeutayMelilla",
        "_GasoleoC",
        "_ElectricidadPeninsular",
        "_GLP",
        "_Carbon",
        "_Biocarburante",
        "_ElectricidadCanarias",
        "_BiomasaPellet",
    )

    def __init__(self, root: etree._Element):
        super().__init__(root)
        self.set_args()

    @property
    def GasNatural(self):
        return get_value(self._find(self._GasNatural))

    @property
    def ElectricidadBaleares(self):
        return get_value(self._find(self._ElectricidadBaleares))

    @property
    def BiomasaOtros(self):
        return get_value(self._find(self._BiomasaOtros))

    @property
    def ElectricidadCeutayMelilla(self):
        return get_value(self._find(self._ElectricidadCeutayMelilla))

    @property
    def GasoleoC(self):
        return get_value(self._find(self._GasoleoC))

    @property
    def ElectricidadPeninsular(self):
        return get_value(self._find(self._ElectricidadPeninsular))

    @property
    def GLP(self):
        return get_value(self._find(self._GLP))

    @property
    def Carbon(self):
        return get_value(self._find(self._Carbon))

    @property
    def Biocarburante(self):
        return get_value(self._find(self._Biocarburante))

    @property
    def ElectricidadCanarias(self):
        return get_value(self._find(self._ElectricidadCanarias))

    @property
    def BiomasaPellet(self):
        return get_value(self._find(self._BiomasaPellet))


class _Parser_FactoresDePaso(object):
    def __init__(self, root: etree._Element) -> None:
        self._root = root.find("FactoresdePaso")

        self.FinalAPrimariaNoRenovable = _Parser_combustibles(self._root.find("FinalAPrimariaNoRenovable"))
        self.FinalAEmisiones = _Parser_combustibles(self._root.find("FinalAEmisiones"))


class _Parser_EnergiaFinalVectores:
    """
    Parsea los datos contenidos en

    <EnergiaFinalVectores> 55.86  </EnergiaFinalVectores>
    <GasNatural> 100.5  </GasNatural>
    <ElectricidadPeninsular> 25.90  </ElectricidadPeninsular>
    <BiomasaOtros> 55.86  </BiomasaOtros>
    <GasoleoC> 55.86  </GasoleoC>
    <GLP> 55.86  </GLP>
    <Carbon> 55.86  </Carbon>
    <Biocarburante> 0.00  </Biocarburante>
    <BiomasaPellet> 0.00  </BiomasaPellet>


    """

    def __init__(self, root: etree._Element) -> None:
        self._root = root.find("EnergiaFinalVectores")

        self.GasNatural = _Parser_instalaciones(self._root.find("GasNatural"))
        self.ElectricidadPeninsular = _Parser_instalaciones(self._root.find("ElectricidadPeninsular"))
        self.BiomasaOtros = _Parser_instalaciones(self._root.find("BiomasaOtros"))
        self.GasoleoC = _Parser_instalaciones(self._root.find("GasoleoC"))
        self.GLP = _Parser_instalaciones(self._root.find("GLP"))
        self.Carbon = _Parser_instalaciones(self._root.find("Carbon"))
        self.Biocarburante = _Parser_instalaciones(self._root.find("Biocarburante"))
        self.BiomasaPellet = _Parser_instalaciones(self._root.find("BiomasaPellet"))


class _Parser_Consumo(object):
    def __init__(self, root: etree._Element):
        self._root = root.find("Consumo")

        self._FactoresdePaso = _Parser_FactoresDePaso
        self._EnergiaFinalVectores = _Parser_EnergiaFinalVectores
        self._EnergiaPrimariaNoRenovable = _Parser_instalaciones

    @property
    def FactoresdePaso(self):
        return self._FactoresdePaso(self._root)

    @property
    def EnergiaFinalVectores(self):
        return self._EnergiaFinalVectores(self._root)

    @property
    def EnergiaPrimariaNoRenovable(self):
        return self._EnergiaPrimariaNoRenovable(self._root.find("EnergiaPrimariaNoRenovable"))


class _Parser_EmisionesCO2(object):
    def __init__(self, root: etree._Element):
        self._root = root.find("EmisionesCO2")

        self._instal = _Parser_instalaciones(self._root)

        self.ConsumoElectrico = get_value(self._root.find("ConsumoElectrico"))
        self.TotalConsumoElectrico = get_value(self._root.find("TotalConsumoElectrico"))
        self.TotalConsumoOtros = get_value(self._root.find("TotalConsumoOtros"))
        self.Calefaccion = self._instal.Calefaccion
        self.Global = self._instal.Global
        self.ACS = self._instal.ACS
        self.Refrigeracion = self._instal.Refrigeracion
        self.ConsumoOtros = get_value(self._root.find("ConsumoOtros"))
        self.Iluminacion = self._instal.Iluminacion


class _Parser_Calificacion(object):
    _Demanda = "Demanda"
    _EPNR = "EnergiaPrimariaNoRenovable"
    _EmisionesCO2 = "EmisionesCO2"

    def __init__(self, root: etree._Element):
        self._root: etree._Element = root.find("Calificacion")
        self._parser_demanda = _Parser_calificacion_demanda
        self._parser_EPNR = _Parser_calificacion_EnergiaPrimariaNoRenovable
        self._parser_EmisionesCO2 = _Parser_calificacion_EmisionesCO2

    @property
    def Demanda(self):
        return self._parser_demanda(self._root.find(self._Demanda))

    @property
    def EnergiaPrimariaNoRenovable(self):
        return self._parser_EPNR(self._root.find(self._EPNR))

    @property
    def EmisionesCO2(self):
        return self._parser_EmisionesCO2(self._root.find(self._EmisionesCO2))


class _Parser_Medida(_Primitive):
    __slots__ = (
        "_CosteEstimado",
        "_CalificacionDemanda",
        "_OtrosDatos",
        "_EnergiaFinal",
        "_CalificacionEnergiaPrimariaNoRenovable",
        "_Demanda",
        "_Descripcion",
        "_Nombre",
        "_EnergiaPrimariaNoRenovable",
        "_EmisionesCO2",
        "_CalificacionEmisionesCO2",
    )

    def __init__(self, root: etree._Element):
        super().__init__(root)
        self.set_args()

    @property
    def CosteEstimado(self):
        return get_value(self._find(self._CosteEstimado))

    @property
    def CalificacionDemanda(self):
        return _Parser_instalaciones(self._find(self._CalificacionDemanda))

    @property
    def OtrosDatos(self):
        return get_value(self._find(self._OtrosDatos))

    @property
    def EnergiaFinal(self):
        return _Parser_instalaciones(self._find(self._EnergiaFinal))

    @property
    def CalificacionEnergiaPrimariaNoRenovable(self):
        return _Parser_instalaciones(self._find(self._CalificacionEnergiaPrimariaNoRenovable))

    @property
    def Demanda(self):
        return _Parser_instalaciones(self._find(self._Demanda))

    @property
    def Descripcion(self):
        return get_value(self._find(self._Descripcion))

    @property
    def Nombre(self):
        return get_value(self._find(self._Nombre))

    @property
    def EnergiaPrimariaNoRenovable(self):
        return _Parser_instalaciones(self._find(self._EnergiaPrimariaNoRenovable))

    @property
    def EmisionesCO2(self):
        return _Parser_instalaciones(self._find(self._EmisionesCO2))

    @property
    def CalificacionEmisionesCO2(self):
        return _Parser_instalaciones(self._find(self._CalificacionEmisionesCO2))


class _Parser_MedidasDeMejora(_Primitive):
    def __init__(self, root: etree._Element):
        super().__init__(root.find("MedidasDeMejora"))

        m1, m2, m3 = self._get_medidas()

        self._m1 = m1
        self._m2 = m2
        self._m3 = m3

    @property
    def Medida_1(self):
        return _Parser_Medida(self._m1)

    @property
    def Medida_2(self):
        return _Parser_Medida(self._m2)

    @property
    def Medida_3(self):
        return _Parser_Medida(self._m3)

    def _get_medidas(self) -> etree._Element:
        """
        Finds all tags with the same name.
        returns.    3 tags always
        """
        return self._root.findall("Medida")


class _Parser_PruebasComprobacionesInspecciones(object):
    def __init__(self, root: etree._Element):
        self._root: etree._Element = root.find("PruebasComprobacionesInspecciones").find("Visita")

        self._Datos = "Datos"
        self._FechaVisita = "FechaVisita"

    @property
    def Datos(self):
        return get_value(self._root.find(self._Datos))

    @property
    def FechaVisita(self):
        text = get_value(self._root.find(self._FechaVisita))
        if text:
            return datetime.strptime(text, "%d/%m/%Y")
        return None


class _Parser_DatosPersonalizados(object):
    def __init__(self, root: etree._Element):
        self._root: etree._Element = root.find("DatosPersonalizados")

        self._Aplicacion = "Aplicacion"
        self._FechaGeneracion = "FechaGeneracion"

    @property
    def Aplicacion(self):
        return get_value(self._root.find(self._Aplicacion))

    @property
    def FechaGeneracion(self):
        text = get_value(self._root.find(self._FechaGeneracion))
        if text:
            return datetime.strptime(text, "%d/%m/%Y")
        return None


class ParserCEX(object):
    def __init__(self, xml: Path | str) -> None:
        self._xml = etree.parse(xml)

        self._DatosDelCertificador = _Parser_DatosDelCertificador
        self._IdentificacionEdificio = _Parser_IdentificacionEdificio
        self._DatosGeneralesyGeometria = _Parser_DatosGeneralesyGeometria
        self._DatosEnvolventeTermica = _Parser_DatosEnvolventeTermica
        self._InstalacionesTermicas = _Parser_InstalacionesTermicas
        self._CondicionesFuncionamientoyOcupacion = _Parser_CondicionesFuncionamientoyOcupacion
        self._Demanda = _Parser_Demanda
        self._Consumo = _Parser_Consumo
        self._EmisionesCO2 = _Parser_EmisionesCO2
        self._Calificacion = _Parser_Calificacion
        self._MedidasDeMejora = _Parser_MedidasDeMejora
        self._PruebasComprobacionesInspecciones = _Parser_PruebasComprobacionesInspecciones
        self._DatosPersonalizados = _Parser_DatosPersonalizados

    @property
    def DatosDelCertificador(self):
        return self._DatosDelCertificador(self._xml)

    @property
    def IdentificacionEdificio(self):
        return self._IdentificacionEdificio(self._xml)

    @property
    def DatosGeneralesyGeometria(self):
        return self._DatosGeneralesyGeometria(self._xml)

    @property
    def DatosEnvolventeTermica(self):
        return self._DatosEnvolventeTermica(self._xml)

    @property
    def InstalacionesTermicas(self):
        return self._InstalacionesTermicas(self._xml)

    @property
    def CondicionesFuncionamientoyOcupacion(self):
        return self._CondicionesFuncionamientoyOcupacion(self._xml)

    @property
    def Demanda(self):
        return self._Demanda(self._xml)

    @property
    def Consumo(self):
        return self._Consumo(self._xml)

    @property
    def EmisionesCO2(self):
        return self._EmisionesCO2(self._xml)

    @property
    def Calificacion(self):
        return self._Calificacion(self._xml)

    @property
    def MedidasDeMejora(self):
        return self._MedidasDeMejora(self._xml)

    @property
    def PruebasComprobacionesInspecciones(self):
        return self._PruebasComprobacionesInspecciones(self._xml)

    @property
    def DatosPersonalizados(self):
        return self._DatosPersonalizados(self._xml)
