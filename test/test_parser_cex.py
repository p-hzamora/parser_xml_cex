from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


import unittest

from parser_cex import ParserCEX, _Parser_instalaciones


xml_path = Path(__file__).parent / "test_cee.xml"
cex = ParserCEX(xml_path)


class TestDatosDelCertificador(unittest.TestCase):
    certificador = cex.DatosDelCertificador

    def test_DatosDelCertificador(self):
        self.assertEqual(self.certificador.NIFEntidad, "B81512550")
        self.assertEqual(self.certificador.ComunidadAutonoma, "Comunidad de Madrid")
        self.assertEqual(self.certificador.Titulacion, "Arquitecto")
        self.assertEqual(self.certificador.Fecha, "25/07/2023")
        self.assertEqual(self.certificador.NIF, "07243977N")
        self.assertEqual(self.certificador.NombreyApellidos, "Rafael Cuenca Herreros")
        self.assertEqual(self.certificador.RazonSocial, "ST Consultores  Inmobiliarios S.L")
        self.assertEqual(self.certificador.Municipio, "Madrid")
        self.assertEqual(self.certificador.CodigoPostal, "28002")
        self.assertEqual(self.certificador.Provincia, "Madrid")
        self.assertEqual(self.certificador.Telefono, "911835430")
        self.assertEqual(self.certificador.Email, "gestionayudas@stconsultores.com")
        self.assertEqual(self.certificador.Domicilio, "Calle Principe de Vergara, 112 6ª planta")


class TestIdentificacionEdificio(unittest.TestCase):
    edificio = cex.IdentificacionEdificio

    def test_IdentificacionEdificio(self):
        self.assertEqual(self.edificio.ReferenciaCatastral, "3558927VK4735H")
        self.assertEqual(self.edificio.Provincia, "Madrid")
        self.assertEqual(self.edificio.ComunidadAutonoma, "Comunidad de Madrid")
        self.assertEqual(self.edificio.ZonaClimatica, "D3")
        self.assertEqual(self.edificio.TipoDeEdificio, "BloqueDeViviendaCompleto")
        self.assertEqual(self.edificio.NormativaVigente, "Anterior a la NBE-CT-79")
        self.assertEqual(self.edificio.Direccion, "CALLE RUIZ PERELLO 8")
        self.assertEqual(self.edificio.NombreDelEdificio, "COMUNIDAD DE PROPIETARIOS DE CALLE RUIZ PERELLO 8")
        self.assertEqual(self.edificio.Procedimiento, "CEXv2.3")
        self.assertEqual(self.edificio.CodigoPostal, "28028")
        self.assertEqual(self.edificio.AlcanceInformacionXML, "CertificacionExistente")
        self.assertEqual(self.edificio.Municipio, "Madrid")
        self.assertEqual(self.edificio.AnoConstruccion, "1960")


class TestCalificacion(unittest.TestCase):
    calificacion = cex.Calificacion

    def test_Demanda(self):
        def EscalaCalefaccion():
            self.assertEqual(demanda.EscalaCalefaccion.A, 11.70)
            self.assertEqual(demanda.EscalaCalefaccion.B, 27.00)
            self.assertEqual(demanda.EscalaCalefaccion.C, 48.70)
            self.assertEqual(demanda.EscalaCalefaccion.D, 81.60)
            self.assertEqual(demanda.EscalaCalefaccion.E, 144.10)
            self.assertEqual(demanda.EscalaCalefaccion.F, 157.10)

        def EscalaRefrigeracion():
            self.assertEqual(demanda.EscalaRefrigeracion.A, 5.50)
            self.assertEqual(demanda.EscalaRefrigeracion.B, 8.90)
            self.assertEqual(demanda.EscalaRefrigeracion.C, 13.90)
            self.assertEqual(demanda.EscalaRefrigeracion.D, 21.30)
            self.assertEqual(demanda.EscalaRefrigeracion.E, 26.30)
            self.assertEqual(demanda.EscalaRefrigeracion.F, 32.40)

        demanda = self.calificacion.Demanda
        self.assertEqual(demanda.Calefaccion, "E")
        self.assertEqual(demanda.Refrigeracion, "B")
        EscalaCalefaccion()
        EscalaRefrigeracion()

    def test_EnergiaPrimariaNoRenovable(self):
        def escala_global():
            self.assertEqual(EPNR.EscalaGlobal.A, 37.10)
            self.assertEqual(EPNR.EscalaGlobal.B, 60.10)
            self.assertEqual(EPNR.EscalaGlobal.C, 93.20)
            self.assertEqual(EPNR.EscalaGlobal.D, 143.30)
            self.assertEqual(EPNR.EscalaGlobal.E, 298.10)
            self.assertEqual(EPNR.EscalaGlobal.F, 336.80)

        EPNR = cex.Calificacion.EnergiaPrimariaNoRenovable
        self.assertEqual(EPNR.Calefaccion, "E")
        self.assertEqual(EPNR.Refrigeracion, "B")
        self.assertEqual(EPNR.ACS, "G")
        self.assertEqual(EPNR.Global, "E")
        escala_global()

    def test_EmisionesCO2(self):
        def escala_global():
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.A, 8.40)
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.B, 13.60)
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.C, 21.10)
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.D, 32.40)
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.E, 66.30)
            self.assertEqual(cex.Calificacion.EmisionesCO2.EscalaGlobal.F, 79.60)

        EmisionesCO2 = cex.Calificacion.EmisionesCO2
        self.assertEqual(EmisionesCO2.Calefaccion, "E")
        self.assertEqual(EmisionesCO2.Refrigeracion, "A")
        self.assertEqual(EmisionesCO2.ACS, "G")
        self.assertEqual(EmisionesCO2.Global, "E")
        escala_global()


class TestDatosGeneralesyGeometria(unittest.TestCase):
    geotermia = cex.DatosGeneralesyGeometria

    def test_DatosGeneralesyGeotermia(self):
        self.assertEqual(self.geotermia.VentilacionUsoResidencial, 0.63)
        self.assertEqual(self.geotermia.NumeroDePlantasSobreRasante, 99999999.99)
        self.assertEqual(self.geotermia.PorcentajeSuperficieHabitableCalefactada, 100)
        self.assertEqual(self.geotermia.SuperficieHabitable, 2214.40)
        self.assertEqual(self.geotermia.DensidadFuentesInternas, 0.00)
        self.assertEqual(self.geotermia.Compacidad, 3.13)
        self.assertEqual(self.geotermia.VolumenEspacioHabitable, 6643.20)
        self.assertEqual(self.geotermia.VentilacionTotal, 0.63)
        self.assertEqual(self.geotermia.DemandaDiariaACS, 2903.60)
        self.assertEqual(self.geotermia.Plano, "plano codificado en Base64")
        self.assertEqual(self.geotermia.NumeroDePlantasBajoRasante, 99999999)
        self.assertEqual(self.geotermia.PorcentajeSuperficieHabitableRefrigerada, 0)
        self.assertEqual(self.geotermia.Imagen, "imagen codificada en Base64")


class TestMedidasDeMejora(unittest.TestCase):
    med_mejora = cex.MedidasDeMejora

    def test_paquete_1(self):
        def test_EnergiaFinal():
            self.assertEqual(medida.EnergiaFinal.ACS, 35.05)
            self.assertEqual(medida.EnergiaFinal.Calefaccion, 89.10)
            self.assertEqual(medida.EnergiaFinal.Global, 127.55)
            self.assertEqual(medida.EnergiaFinal.Refrigeracion, 3.40)
            self.assertEqual(medida.EnergiaFinal.Iluminacion, 0.00)
            self.assertEqual(medida.EnergiaFinal.GlobalDiferenciaSituacionInicial, None)

        def test_CalificacionEnergiaPrimariaNoRenovable():
            self.assertEqual(medida.CalificacionEnergiaPrimariaNoRenovable.ACS, "G")
            self.assertEqual(medida.CalificacionEnergiaPrimariaNoRenovable.Calefaccion, "D")
            self.assertEqual(medida.CalificacionEnergiaPrimariaNoRenovable.Global, "E")
            self.assertEqual(medida.CalificacionEnergiaPrimariaNoRenovable.Refrigeracion, "B")

        def test_Demanda():
            self.assertEqual(medida.Demanda.Calefaccion, 65.76)
            self.assertEqual(medida.Demanda.Global, 98.43)
            self.assertEqual(medida.Demanda.GlobalDiferenciaSituacionInicial, 66.23)
            self.assertEqual(medida.Demanda.Refrigeracion, 6.80)

        def test_EnergiaPrimariaNoRenovable():
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.GlobalDiferenciaSituacionInicial, 105.94)
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.Calefaccion, 106.03)
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.Global, 154.39)
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.ACS, 41.71)
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.Iluminacion, 0.00)
            self.assertEqual(medida.EnergiaPrimariaNoRenovable.Refrigeracion, 6.64)

        def test_EmisionesCO2():
            self.assertEqual(medida.EmisionesCO2.GlobalDiferenciaSituacionInicial, 22.38)
            self.assertEqual(medida.EmisionesCO2.Calefaccion, 22.45)
            self.assertEqual(medida.EmisionesCO2.Global, 32.41)
            self.assertEqual(medida.EmisionesCO2.ACS, 8.83)
            self.assertEqual(medida.EmisionesCO2.Iluminacion, 0.00)
            self.assertEqual(medida.EmisionesCO2.Refrigeracion, 1.13)

        def test_CalificacionEmisionesCO2():
            self.assertEqual(medida.CalificacionEmisionesCO2.ACS, "G")
            self.assertEqual(medida.CalificacionEmisionesCO2.Calefaccion, "D")
            self.assertEqual(medida.CalificacionEmisionesCO2.Global, "E")
            self.assertEqual(medida.CalificacionEmisionesCO2.Refrigeracion, "A")

        # ______start___________
        medida = self.med_mejora.Medida_1
        self.assertEqual(medida.CosteEstimado, "-")
        self.assertEqual(medida.CalificacionDemanda.Calefaccion, "D")
        self.assertEqual(medida.CalificacionDemanda.Refrigeracion, "B")
        self.assertEqual(medida.OtrosDatos, None)

        test_EnergiaFinal()
        test_CalificacionEnergiaPrimariaNoRenovable()

        self.assertEqual(medida.Descripcion, "Aislamiento exterior de 3 cm de XPS 0.034W/mK en Fachadas")
        self.assertEqual(medida.Nombre, "Paquete LIGHT(30-45 %)")

        test_Demanda()
        test_EnergiaPrimariaNoRenovable()
        test_EmisionesCO2()
        test_CalificacionEmisionesCO2()


class TestInstalacionesTermicas(unittest.TestCase):
    instalaciones = cex.InstalacionesTermicas

    def test_GeneradoresDeCalefaccion(self):
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.RendimientoNominal, 99999999.99)
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.Tipo, "Caldera Estándar")
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.ModoDeObtencion, "Estimado")
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.VectorEnergetico, "GasNatural")
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.PotenciaNominal, 300.00)
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.Nombre, "Calefacción y ACS")
        self.assertEqual(self.instalaciones.GeneradoresDeCalefaccion.RendimientoEstacional, 0.74)

    def test_InstalacionesACS(self):
        self.assertEqual(self.instalaciones.InstalacionesACS.RendimientoNominal, 99999999.99)
        self.assertEqual(self.instalaciones.InstalacionesACS.Tipo, "Caldera Estándar")
        self.assertEqual(self.instalaciones.InstalacionesACS.ModoDeObtencion, "Estimado")
        self.assertEqual(self.instalaciones.InstalacionesACS.VectorEnergetico, None)
        self.assertEqual(self.instalaciones.InstalacionesACS.PotenciaNominal, 300.00)
        self.assertEqual(self.instalaciones.InstalacionesACS.Nombre, "Calefacción y ACSanitaria")
        self.assertEqual(self.instalaciones.InstalacionesACS.RendimientoEstacional, 0.74)

    # def test_Consumo_EPNR(self):

    #     self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.ACS, )
    #     self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Calefaccion, )
    #     self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Global, )
    #     self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Refrigeracion, )
    #     self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Iluminacion, )


class TestCondicionesFuncionamientoyOcupacion(unittest.TestCase):
    condiciones = cex.CondicionesFuncionamientoyOcupacion

    def test_CondicionesFuncionamientoyOcupacion(self):
        self.assertEqual(self.condiciones.Nombre, "Edificio Objeto")
        self.assertEqual(self.condiciones.Superficie, 2214.40)
        self.assertEqual(self.condiciones.NivelDeAcondicionamiento, "Acondicionado")
        self.assertEqual(self.condiciones.PerfilDeUso, "residencial-24h-baja")


class TestDemanda(unittest.TestCase):
    demanda = cex.Demanda.EdificioObjeto

    def test_demanda(self):
        self.assertEqual(self.demanda.Global, 164.65)
        self.assertEqual(self.demanda.ACS, 25.87)
        self.assertEqual(self.demanda.Refrigeracion, 8.12)
        self.assertEqual(self.demanda.Calefaccion, 130.66)
        self.assertEqual(self.demanda.Conjunta, 136.34)


class TestConsumo(unittest.TestCase):
    def test_factores_de_paso(self):
        def finalEmisiones():
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.GasNatural, 0.252)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.ElectricidadBaleares, 0.331)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.BiomasaOtros, 0.018)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.ElectricidadCeutayMelilla, 0.331)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.GasoleoC, 0.311)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.ElectricidadPeninsular, 0.331)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.GLP, 0.254)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.Carbon, 0.472)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.Biocarburante, 0.018)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.ElectricidadCanarias, 0.331)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAEmisiones.BiomasaPellet, 0.018)

        def finalPrimariaNoRenovable():
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.GasNatural, 1.19)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.ElectricidadBaleares, 1.954)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.BiomasaOtros, 0.034)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.ElectricidadCeutayMelilla, 1.954)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.GasoleoC, 1.179)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.ElectricidadPeninsular, 1.954)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.GLP, 1.201)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.Carbon, 1.082)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.Biocarburante, 0.085)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.ElectricidadCanarias, 1.954)
            self.assertEqual(cex.Consumo.FactoresdePaso.FinalAPrimariaNoRenovable.BiomasaPellet, 0.085)

        finalEmisiones()
        finalPrimariaNoRenovable()

    def test_EnergiaFinalVectores(self):
        EnergiaFinalVectores = cex.Consumo.EnergiaFinalVectores

        def test_0(arg):
            property: _Parser_instalaciones = getattr(EnergiaFinalVectores, arg)
            self.assertEqual(property.Calefaccion, 0.00)
            self.assertEqual(property.Global, 0.00)
            self.assertEqual(property.ACS, 0.00)
            self.assertEqual(property.Refrigeracion, 0.00)
            self.assertEqual(property.Iluminacion, 0.00)

        def test_GasNatural():
            self.assertEqual(EnergiaFinalVectores.GasNatural.Calefaccion, 177.04)
            self.assertEqual(EnergiaFinalVectores.GasNatural.Global, 212.10)
            self.assertEqual(EnergiaFinalVectores.GasNatural.ACS, 35.05)
            self.assertEqual(EnergiaFinalVectores.GasNatural.Refrigeracion, 0.00)
            self.assertEqual(EnergiaFinalVectores.GasNatural.Iluminacion, 0.00)

        def test_ElectricidadPeninsular():
            self.assertEqual(EnergiaFinalVectores.ElectricidadPeninsular.Calefaccion, 0.00)
            self.assertEqual(EnergiaFinalVectores.ElectricidadPeninsular.Global, 4.06)
            self.assertEqual(EnergiaFinalVectores.ElectricidadPeninsular.ACS, 0.00)
            self.assertEqual(EnergiaFinalVectores.ElectricidadPeninsular.Refrigeracion, 4.06)
            self.assertEqual(EnergiaFinalVectores.ElectricidadPeninsular.Iluminacion, 0.00)

        test_GasNatural()
        test_ElectricidadPeninsular()
        test_0("BiomasaOtros")
        test_0("GasoleoC")
        test_0("GLP")
        test_0("Carbon")
        test_0("Biocarburante")
        test_0("BiomasaPellet")

    def test_EnergiaPrimariaNoRenovable(self):
        self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.ACS, 41.71)
        self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Calefaccion, 210.68)
        self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Global, 260.33)
        self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Refrigeracion, 7.94)
        self.assertEqual(cex.Consumo.EnergiaPrimariaNoRenovable.Iluminacion, 0.00)


class TestDatosPersonalizados(unittest.TestCase):
    def test_datosPersonalizados(self):
        self.assertEqual(cex.DatosPersonalizados.Aplicacion, "CE3X")
        self.assertEqual(cex.DatosPersonalizados.FechaGeneracion, datetime(2023, 7, 26))


class TestPruebasComprobacionesInspecciones(unittest.TestCase):
    def test_PruebasComprobacionesInspecciones(self):
        self.assertEqual(cex.PruebasComprobacionesInspecciones.Datos, None)
        self.assertEqual(cex.PruebasComprobacionesInspecciones.FechaVisita, datetime(2023, 7, 25))


class TestDatosEnvolventeTermica(unittest.TestCase):
    Envolvente = cex.DatosEnvolventeTermica

    def test_CerramientosOpacos(self):
        self.Envolvente.CerramientosOpacos.df

    def test_HuecosyLucernarios(self):
        self.Envolvente.HuecosyLucernarios.df
        pass

    def test_PuentesTermicos(self):
        self.Envolvente.PuentesTermicos.df
        pass


if __name__ == "__main__":
    unittest.main()

    # DatosEnvolventeTermica CerramientosOpacos elementos
    elementos = cex.DatosEnvolventeTermica.CerramientosOpacos.elementos
    elementos[0].Tipo
    elementos[0].ModoDeObtencion
    elementos[0].Transmitancia
    elementos[0].Nombre
    elementos[0].Orientacion
    elementos[0].Superficie

    elementos[5].Tipo
    elementos[5].ModoDeObtencion
    elementos[5].Transmitancia
    elementos[5].Nombre
    elementos[5].Orientacion
    elementos[5].Superficie

    # DatosEnvolventeTermica PuentesTermicos elementos
    elementos = cex.DatosEnvolventeTermica.PuentesTermicos.elementos
    elementos[0].Nombre
    elementos[0].ModoDeObtencion
    elementos[0].Transmitancia
    elementos[0].Tipo
    elementos[0].Longitud

    elementos[5].Nombre
    elementos[5].ModoDeObtencion
    elementos[5].Transmitancia
    elementos[5].Tipo
    elementos[5].Longitud

    # DatosEnvolventeTermica HuecosyLucernarios elementos
    elementos = cex.DatosEnvolventeTermica.HuecosyLucernarios.elementos
    elementos[0].Tipo
    elementos[0].Superficie
    elementos[0].Transmitancia
    elementos[0].Nombre
    elementos[0].ModoDeObtencionTransmitancia
    elementos[0].Orientacion
    elementos[0].ModoDeObtencionFactorSolar
    elementos[0].FactorSolar

    elementos[5].Tipo
    elementos[5].Superficie
    elementos[5].Transmitancia
    elementos[5].Nombre
    elementos[5].ModoDeObtencionTransmitancia
    elementos[5].Orientacion
    elementos[5].ModoDeObtencionFactorSolar
    elementos[5].FactorSolar
