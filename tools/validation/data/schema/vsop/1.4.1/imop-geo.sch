<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="geo" uri="https://standaarden.overheid.nl/stop/imop/geo/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:ns prefix="basisgeo" uri="http://www.geostandaarden.nl/basisgeometrie/1.0"/>
   <sch:ns prefix="gml" uri="http://www.opengis.net/gml/3.2"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validatie voor imop-geo.xsd</sch:p>
   <sch:pattern id="sch_geo_001">
      <sch:title>Locatie rules voor GIO-versie of GIO-mutatie</sch:title>
      <sch:rule context="geo:locaties | geo:locatieMutaties">
         <sch:let name="aantalLocaties"
                  value="count(./geo:Locatie) + count(./geo:LocatieMutatie)"/>
         <sch:let name="aantalLocatiesMetGroepID"
                  value="count(./geo:Locatie/geo:groepID) + count(./geo:LocatieMutatie/geo:groepID)"/>
         <sch:let name="aantalLocatiesMetKwantitatieveNormwaarde"
                  value="count(./geo:Locatie/geo:kwantitatieveNormwaarde) + count(./geo:LocatieMutatie/geo:kwantitatieveNormwaarde)"/>
         <sch:let name="aantalLocatiesMetKwalitatieveNormwaarde"
                  value="count(./geo:Locatie/geo:kwalitatieveNormwaarde) + count(./geo:LocatieMutatie/geo:kwalitatieveNormwaarde)"/>
         <sch:let name="Expressie"
                  value="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
         <sch:p>
				Als er één locatie is in een GIO waar een waarde groepID is ingevuld MOETEN ze allemaal
				zijn ingevuld.
			</sch:p>
         <sch:assert id="STOP3000"
                     test="($aantalLocatiesMetGroepID = 0) or ($aantalLocatiesMetGroepID = $aantalLocaties)"
                     role="fout">
				{"code": "STOP3000", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Als er 1 locatie is in een GIO waar een waarde groepID is ingevuld moet elke locatie een GroepID hebben. Geef alle locaties een groepID (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:assert>
         <sch:p>
				Als er één locatie is in een GIO waar kwantitatieveNormwaarde is ingevuld MOETEN alle
				locaties een kwantitatieveNormWaarde hebben.
			</sch:p>
         <sch:assert id="STOP3006"
                     test="($aantalLocatiesMetKwantitatieveNormwaarde = 0) or ($aantalLocatiesMetKwantitatieveNormwaarde = $aantalLocaties)"
                     role="fout">
				{"code": "STOP3006", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Een locatie heeft een kwantitatieveNormwaarde, en één of meerdere andere locaties niet. Geef alle locaties een kwantitatieveNormwaarde, of verwijder alle kwantitatieveNormwaardes (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:assert>
         <sch:p>
				Als er één locatie is in een GIO waar kwalitatieveNormwaarde is ingevuld MOETEN alle
				locaties een kwalitatieveNormwaarde hebben.
			</sch:p>
         <sch:assert id="STOP3007"
                     test="($aantalLocatiesMetKwalitatieveNormwaarde = 0) or ($aantalLocatiesMetKwalitatieveNormwaarde = $aantalLocaties)"
                     role="fout">
				{"code": "STOP3007", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Een locatie heeft een kwalitatieveNormwaarde, en één of meerdere andere locaties niet. Geef alle locaties een kwalitatieveNormwaarde, of verwijder alle kwalitatieveNormwaardes (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:assert>
         <sch:p>
				Als de locaties van de GIO kwantitatieve normwaarden hebben, moet de
				eenheid(eenheidlabel en eenheidID) aanwezig zijn in de GIO.
			</sch:p>
         <sch:report id="STOP3009"
                     test="(($aantalLocatiesMetKwantitatieveNormwaarde gt 0) and ((not(exists(../geo:eenheidlabel))) or (not(exists(../geo:eenheidID)))))"
                     role="fout">
				{"code": "STOP3009", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "De locaties bevatten kwantitatieve normwaarden, terwijl eenheidlabel en/of eenheidID ontbreken. Vul deze aan (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:report>
         <sch:p>
				Als de locaties van de GIO kwalitatieve normwaarden hebben, MOGEN eenheidlabel en
				eenheidID NIET voorkomen.
			</sch:p>
         <sch:report id="STOP3015"
                     test="(($aantalLocatiesMetKwalitatieveNormwaarde gt 0) and ((exists(../geo:eenheidlabel) or exists(../geo:eenheidID))))"
                     role="fout">
				{"code": "STOP3015", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Het GIO met kwalitatieve normwaarden mag geen eenheidlabel noch eenheidID hebben. Verwijder eenheidlabel en eenheidID toe, of verander de kwalitatieve in kwantitatieve normwaarden (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:report>
         <sch:p>
				Als de locaties van de GIO kwantitatieve òf kwalitatieve normwaarden hebben, dan moet
				de norm (normlabel en normID) aanwezig zijn.
			</sch:p>
         <sch:report id="STOP3011"
                     test="((($aantalLocatiesMetKwantitatieveNormwaarde + $aantalLocatiesMetKwalitatieveNormwaarde) gt 0) and ((not(exists(../geo:normlabel))) or (not(exists(../geo:normID)))))"
                     role="fout">
				{"code": "STOP3011", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "De locaties bevatten wel kwantitatieve òf kwalitatieve normwaarden, maar geen norm. Vul normlabel en normID aan (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_3013">
      <sch:rule context="geo:locaties">
         <sch:p>
				Binnen <codeph>geo:locaties</codeph> in een GIO-versie mag elke basisgeo:id (GUID) van de geometrische data van een locatie maar
				één keer voorkomen.
			</sch:p>
         <sch:assert id="STOP3013"
                     test="count(./geo:Locatie/geo:geometrie/basisgeo:Geometrie/basisgeo:id) = count(distinct-values(./geo:Locatie/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"
                     role="fout">
				{"code": "STOP3013", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>", "melding": "De basisgeo:id's van de locaties zijn niet uniek. Binnen 1 GIO-versie mag basisgeo:id van geometrische objecten van verschillende locaties niet gelijk zijn aan elkaar. Pas dit aan (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_3032">
      <sch:rule context="geo:locatieMutaties">
         <sch:p>
				De <codeph>geo:locatieMutaties</codeph> in een GIO-wijziging MOETEN er in de
				resulterende GIO-versie toe leiden dat elke basisgeo:id (GUID) van de 
				geometrische data van een locatie maar één keer voorkomet.
			</sch:p>
         <sch:let name="voegtoe"
                  value="count(geo:LocatieMutatie[geo:wijzigactie='voegtoe' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id)"/>
         <sch:let name="voegtoeDis"
                  value="count(distinct-values(geo:LocatieMutatie[geo:wijzigactie='voegtoe' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
         <sch:let name="verwijder"
                  value="count(geo:LocatieMutatie[geo:wijzigactie='verwijder' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id)"/>
         <sch:let name="verwijderDis"
                  value="count(distinct-values(geo:LocatieMutatie[geo:wijzigactie='verwijder' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
         <sch:assert id="STOP3032"
                     test="$voegtoe = $voegtoeDis and $verwijder = $verwijderDis"
                     role="fout">
				{"code": "STOP3032", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "melding": "De geo:locatieMutaties leiden tot niet unieke basisgeo:id's van de locaties in de nieuwe GIO-versie. Binnen 1 GIO-versie mogen de basisgeo:id's van geometrische objecten van verschillende locaties niet gelijk zijn aan elkaar. Pas dit aan (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_3034">
      <sch:rule context="geo:wijzigmarkeringen">
         <sch:p>
				Binnen <codeph>geo:wijzigmarkeringen</codeph> MAG elke basisgeo:id (GUID) van de 
				geometrische data maar één keer voorkomen.
			</sch:p>
         <sch:assert id="STOP3034"
                     test="count(.//geo:geometrie/basisgeo:Geometrie/basisgeo:id) = count(distinct-values(.//geo:geometrie/basisgeo:Geometrie/basisgeo:id))"
                     role="fout">
				{"code": "STOP3034", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "melding": "De basisgeo:id's van de geometrieen in de geo:wijzigmarkeringen zijn niet uniek. Omdat de wijzigmarkeringen elkaar niet mogen overlappen, mogen de basisgeo:id's van geometrische objecten niet gelijk zijn aan elkaar. Pas dit aan (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_3008">
      <sch:rule context="geo:Locatie | geo:LocatieMutatie">
         <sch:let name="ID" value="geo:geometrie/basisgeo:Geometrie/basisgeo:id"/>
         <sch:let name="Expressie"
                  value="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
         <sch:p>
				Van de elementen kwalitatieveNormwaarde en kwantitatieveNormwaarde in een Locatie mag
				er slechts één ingevuld zijn.
			</sch:p>
         <sch:assert id="STOP3008"
                     test="count(geo:kwantitatieveNormwaarde) + count(geo:kwalitatieveNormwaarde) le 1"
                     role="fout">
				{"code": "STOP3008", "ID": "<sch:value-of select="$ID"/>", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Locatie met basisgeo:id <sch:value-of select="$ID"/> heeft zowel een kwalitatieveNormwaarde als een kwantitatieveNormwaarde. Verwijder één van beide (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:assert>
         <sch:p>
				Een Locatie binnen een GIO mag niet zowel een groepID (GIO-deel) als een (kwalitatieve
				of kwantitatieve) Normwaarde bevatten.
			</sch:p>
         <sch:report id="STOP3012"
                     test="exists(geo:groepID) and (exists(geo:kwalitatieveNormwaarde) or exists(geo:kwantitatieveNormwaarde))"
                     role="fout">
				{"code": "STOP3012", "ID": "<sch:value-of select="$ID"/>", "ExpressieID": "<sch:value-of select="$Expressie"/>", "melding": "Locatie met basisgeo:id <sch:value-of select="$ID"/> heeft zowel een groepID (GIO-deel) als een (kwalitatieve of kwantitatieve) Normwaarde. Verwijder de Normwaarde of de groepID (GIO <sch:value-of select="$Expressie"/>).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_3010">
      <sch:rule context="geo:kwalitatieveNormwaarde">
         <sch:p>Een kwalitatieveNormwaarde mag geen lege string (“”) zijn.</sch:p>
         <sch:assert id="STOP3010" test="normalize-space(.)" role="fout">
				{"code": "STOP3010", "ID": "<sch:value-of select="../geo:geometrie/basisgeo:Geometrie/basisgeo:id"/>", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "melding": "De kwalitatieveNormwaarde van locatie met basisgeo:id <sch:value-of select="../geo:geometrie/basisgeo:Geometrie/basisgeo:id"/> is niet gevuld. Vul deze aan (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_002">
      <sch:title>
			Als een locatie een groepID heeft, dan MOET deze voorkomen in het lijstje
			groepen.
		</sch:title>
      <sch:rule context="geo:Locatie/geo:groepID | geo:LocatieMutatie/geo:groepID">
         <sch:let name="doelwit" value="./string()"/>
         <sch:p>
				Als een locatie een groepID heeft, dan MOET deze voorkomen in het lijstje
				groepen.
			</sch:p>
         <sch:assert id="STOP3001"
                     test="count(../../../geo:groepen/geo:Groep[geo:groepID = $doelwit]) gt 0"
                     role="fout">
				{"code": "STOP3001", "ID": "<sch:value-of select="$doelwit"/>", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "melding": "Als een locatie een groepID heeft, dan MOET deze voorkomen in het lijstje groepen. GroepID <sch:value-of select="$doelwit"/> komt niet voor in groepen. Geef alle locaties een groepID die voorkomt in groepen (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!-- STOP3002 verwijderd, schema maakt lege waarden voor groepID al onmogelijk -->
   <sch:pattern id="sch_geo_004">
      <sch:title>Check op unieke labels en groepIDs.</sch:title>
      <sch:rule context="geo:groepen">
         <sch:p>Twee groepIDs in het lijstje groepen mogen niet dezelfde waarde hebben.</sch:p>
         <sch:let name="GroepIDs">
            <xsl:for-each select="geo:Groep">
               <xsl:sort select="normalize-space(geo:groepID/./string())"/>
               <ID>
                  <xsl:value-of select="geo:groepID/string()"/>
               </ID>
            </xsl:for-each>
         </sch:let>
         <sch:let name="DubbeleGroepen">
            <xsl:for-each select="$GroepIDs/ID">
               <xsl:if test="preceding::ID[1] = .">
                  <dubbel>
							(<xsl:value-of select="./string()"/>, <xsl:value-of select="preceding::ID[1]/string()"/>)
						</dubbel>
                  <xsl:text> </xsl:text>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP3003"
                     test="normalize-space($DubbeleGroepen) = ''"
                     role="fout">
				{"code": "STOP3003", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "Dubbel": "<sch:value-of select="$DubbeleGroepen/normalize-space()"/>", "melding": "GroepID <sch:value-of select="$DubbeleGroepen/normalize-space()"/> komt meerdere keren voor. Zorg dat iedere Groep een uniek ID heeft (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
         <sch:let name="Labels">
            <xsl:for-each select="geo:Groep">
               <xsl:sort select="normalize-space(geo:label/./string())"/>
               <naam>
                  <xsl:value-of select="geo:label"/>
               </naam>
            </xsl:for-each>
         </sch:let>
         <sch:let name="DubbeleLabels">
            <xsl:for-each select="$Labels/naam">
               <xsl:if test="preceding::naam[1] = .">
						(<xsl:value-of select="./string()"/>, <xsl:value-of select="preceding::naam[1]/string()"/>)
					</xsl:if>
               <xsl:text> </xsl:text>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP3004"
                     test="normalize-space($DubbeleLabels) = ''"
                     role="fout">
				{"code": "STOP3004", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "Dubbel": "<sch:value-of select="$DubbeleLabels/normalize-space()"/>", "melding": "Het label <sch:value-of select="$DubbeleLabels/normalize-space()"/> meerdere keren voor in het lijstje met groepen. Geef unieke labels. (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>)", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_005">
      <sch:title>
			Als een groepID voorkomt in het lijstje groepen dan MOET er minstens 1 locatie zijn
			met dat groepID.
		</sch:title>
      <sch:rule context="geo:groepen/geo:Groep/geo:groepID">
         <sch:let name="doelwit" value="./string()"/>
         <sch:p>
				Als een groepID voorkomt in het lijstje groepen dan MOET er minstens 1 locatie zijn met
				dat groepID.
			</sch:p>
         <sch:assert id="STOP3005"
                     test="count(../../../geo:locaties/geo:Locatie[./geo:groepID = $doelwit]) gt 0 or count(../../../geo:locatieMutaties/geo:LocatieMutatie[./geo:groepID = $doelwit]) gt 0"
                     role="fout">
				{"code": "STOP3005", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "ID": "<sch:value-of select="$doelwit"/>", "melding": "GroepID <sch:value-of select="$doelwit"/> wordt niet gebruikt voor een locatie. Verwijder deze groep, of gebruik de groep bij een Locatie (GIO <sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <sch:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_geo_006">
      <sch:title>Geen norm elementen in een GIO zonder normwaarde.</sch:title>
      <sch:rule context="geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie">
         <sch:p>
				In een GIO waar locaties geen kwalitatieve of kwantitatieve normwaarde hebben, MOGEN
				eenheidID, eenheidlabel, normID en normlabel NIET voorkomen.
			</sch:p>
         <sch:report id="STOP3016"
                     test="(exists(geo:normID) or exists(geo:normlabel) or exists(geo:eenheidID) or exists(geo:eenheidlabel)) and (count(geo:locaties/geo:Locatie/geo:kwantitatieveNormwaarde) = 0 and count(geo:locaties/geo:Locatie/geo:kwalitatieveNormwaarde) = 0) and (count(geo:locatieMutaties/geo:LocatieMutatie/geo:kwantitatieveNormwaarde) = 0 and count(geo:locatieMutaties/geo:LocatieMutatie/geo:kwalitatieveNormwaarde) = 0)"
                     role="fout">
				{"code": "STOP3016", "ExpressieID": "<sch:value-of select="geo:FRBRExpression"/>", "melding": "Het GIO bevat norm (normID en normlabel) en/of eenheid (eenheidID en eenheidlabel), terwijl kwantitatieve of kwalitatieve normwaarden ontbreken. Geef de locaties normwaarden of verwijder de norm/eenheid-elementen (GIO <sch:value-of select="geo:FRBRExpression"/>).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <!-- STOP3017 verwijderd -->
   <!-- STOP3018 kan niet gevalideerd worden -->
   <sch:pattern id="sch_basisgeo_001">
      <sch:title>
			Locaties in een GIO MOETEN een geometrie hebben. (basisgeo:geometrie in
			basisgeo:Geometrie MAG NIET ontbreken of leeg zijn).
		</sch:title>
      <sch:rule context="basisgeo:geometrie">
         <sch:let name="coordinaten">
            <xsl:for-each select=".//gml:posList | .//gml:pos | .//gml:coordinates">
               <xsl:value-of select="./string()"/>
               <xsl:text> </xsl:text>
            </xsl:for-each>
         </sch:let>
         <sch:let name="kenmerk">
            <xsl:if test="name(../../..) = 'geo:Locatie'">(naam='<xsl:value-of select="ancestor::geo:Locatie/geo:naam"/>') in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(../../..) = 'geo:LocatieMutatie'">(naam='<xsl:value-of select="ancestor::geo:LocatieMutatie/geo:naam"/>') in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(../../..) = 'geo:Punt'">(punt in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(../../..) = 'geo:Lijn'">(lijn in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(../../..) = 'geo:Vlak'">(vlak in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(../../..) = 'geo:Gebied'">(label='<xsl:value-of select="ancestor::geo:Gebied/geo:label"/>')</xsl:if>
         </sch:let>
         <sch:assert id="STOP3019"
                     test="(descendant::gml:pos or descendant::gml:posList or descendant::gml:coordinates) and matches($coordinaten, '\d')"
                     role="fout">
				{"code": "STOP3019", "basisgeo:id": "<sch:value-of select="preceding-sibling::basisgeo:id"/>", "Parent": "<sch:value-of select="node-name(../../..)"/>", "Kenmerk": "<sch:value-of select="$kenmerk"/>", "melding": "<sch:value-of select="node-name(../../..)"/>
            <sch:value-of select="$kenmerk"/> met basisgeo:geometrie (<sch:value-of select="preceding-sibling::basisgeo:id"/>) heeft geen of een lege geometrie. Basisgeo:Geometrie zonder geometrische data is niet toegestaan. Voeg een (correcte) basisgeo:geometrie toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_001">
      <sch:title>
			Coördinaten in geometrieen in een GIO MOETEN gebruik maken van het RD of ETRS89
			ruimtelijke referentiesysteem(srsName='urn:ogc:def:crs:EPSG::28992' of
			srsName='urn:ogc:def:crs:EPSG::4258').
		</sch:title>
      <sch:rule context="geo:locaties//gml:*[@srsName] | geo:locatieMutaties//gml:*[@srsName] | geo:wijzigmarkeringen//gml:*[@srsName]">
         <sch:assert id="STOP3020"
                     test="@srsName = 'urn:ogc:def:crs:EPSG::28992' or @srsName = 'urn:ogc:def:crs:EPSG::4258'"
                     role="fout">
				{"code": "STOP3020", "srsName": "<sch:value-of select="@srsName"/>", "ExpressieID": "<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>", "melding": "Het GIO (<sch:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>) bevat een geometrisch object met een ongeldige srsName (<sch:value-of select="@srsName"/>). Alleen srsName='urn:ogc:def:crs:EPSG::28992' of srsName='urn:ogc:def:crs:EPSG::4258' is toegestaan. Wijzig de srsName.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3021">
      <sch:title>Alle srsNames identiek</sch:title>
      <sch:rule context="geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie">
         <sch:let name="srsName" value="//@srsName"/>
         <sch:assert id="STOP3021"
                     test="count(distinct-values(//@srsName)) = 1"
                     role="fout">
				{"code": "STOP3021", "srsNames": "<sch:value-of select="distinct-values($srsName)"/>", "ExpressieID": "<sch:value-of select="geo:FRBRExpression"/>", "melding": "In GIO (<sch:value-of select="geo:FRBRExpression"/>) heeft niet elk geometrisch object dezelfde srsName (<sch:value-of select="distinct-values($srsName)"/>). Dit is niet toegestaan. Zorg ervoor dat elke geometrisch object in het GIO hetzelfde ruimtelijke referentiesysteem (srsName) gebruikt.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3040">
      <sch:title>Geen cirkels en bogen in de basisgeometrie</sch:title>
      <sch:rule context="basisgeo:Geometrie//gml:Circle | basisgeo:Geometrie//gml:Arc | basisgeo:Geometrie//gml:CircleByCenterPoint">
         <sch:report id="STOP3040" test="." role="fout">
				{"code": "STOP3040", "Element": "<sch:value-of select="string(node-name(.))"/>", "id": "<sch:value-of select="ancestor::basisgeo:Geometrie/basisgeo:id"/>", "melding": "De basisgeo:Geometrie(basisgeo:id <sch:value-of select="ancestor::basisgeo:Geometrie/basisgeo:id"/>) bevat een gml aanduiding voor een cirkel of boog (<sch:value-of select="string(node-name(.))"/>). Dit is niet toegestaan. Verwijder <sch:value-of select="string(node-name(.))"/>.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3050">
      <sch:title>
			Coördinaten in geometrieen in een geo:Gebied MOETEN gebruik maken van het RD
			ruimtelijke referentiesysteem(srsName='urn:ogc:def:crs:EPSG::28992').
		</sch:title>
      <sch:rule context="geo:Gebied//gml:*[@srsName]">
         <sch:assert id="STOP3050"
                     test="@srsName = 'urn:ogc:def:crs:EPSG::28992'"
                     role="fout">
				{"code": "STOP3050", "srsName": "<sch:value-of select="@srsName"/>", "label": "<sch:value-of select="ancestor::geo:Gebied/geo:label"/>", "melding": "geo:Gebied(label: <sch:value-of select="ancestor::geo:Gebied/geo:label"/>) bevat een geometrisch object met een ongeldige srsName (<sch:value-of select="@srsName"/>). Alleen srsName='urn:ogc:def:crs:EPSG::28992' is toegestaan. Wijzig de srsName.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3060">
      <sch:title>Effectgebied bevat een vlak in de basisgeometrie</sch:title>
      <sch:rule context="basisgeo:geometrie[ancestor::geo:Effectgebied]">
         <sch:assert id="STOP3060" test=".//gml:Surface or .//gml:Polygon" role="fout">
				{"code": "STOP3060", "Element": "<sch:value-of select="string(node-name(./gml:*))"/>", "label": "<sch:value-of select="string(ancestor::geo:Gebied/geo:label)"/>", "id": "<sch:value-of select="string(ancestor::basisgeo:Geometrie/basisgeo:id)"/>", "melding": "Het Effectgebied met geo:label='<sch:value-of select="string(ancestor::geo:Gebied/geo:label)"/>' bevat een basisgeo:Geometrie(id=<sch:value-of select="string(ancestor::basisgeo:Geometrie/basisgeo:id)"/>) met gml aanduiding (<sch:value-of select="string(node-name(./gml:*))"/>) in plaats van een gml aanduiding voor een vlak. Dit is niet toegestaan. Vervang <sch:value-of select="string(node-name(./gml:*))"/> door gml:Surface of gml:Polygon.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3065">
      <sch:title>Gebiedsmarkering bevat òf ambtsgebied òf een of meer gebied-en</sch:title>
      <sch:rule context="geo:Gebiedsmarkering">
         <sch:report id="STOP3065" test="geo:Gebied and geo:Ambtsgebied" role="fout">
				{"code": "STOP3065", "bgCode": "<sch:value-of select="string(geo:Ambtsgebied/geo:bevoegdGezag)"/>", "aantal": "<sch:value-of select="string(count(child::geo:Gebied))"/>", "label": "<sch:value-of select="string(child::geo:Gebied[1]/geo:label)"/>", "melding": "Gebiedsmarkering bevat een combinatie van geo:Ambtsgebied (met geo:bevoegdGezag <sch:value-of select="string(geo:Ambtsgebied/geo:bevoegdGezag)"/>) en <sch:value-of select="string(count(child::geo:Gebied))"/>x geo:Gebied (eerste gebied heeft geo:label='<sch:value-of select="string(child::geo:Gebied[1]/geo:label)"/>'). Dit is niet toegestaan. Verwijder òf het geo:Ambtsgebied òf ALLE geo:Gebied-en.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_3080">
      <sch:title>Een GIO-mutatie MOET een was-ID verwijzing hebben.</sch:title>
      <sch:rule context="geo:GeoInformatieObjectVaststelling/geo:vastgesteldeVersie/geo:GeoInformatieObjectMutatie">
         <sch:assert id="STOP3080"
                     test="ancestor::geo:GeoInformatieObjectVaststelling/geo:wasID"
                     role="fout">
				{"code": "STOP3080", "ExpressieID": "<sch:value-of select="geo:FRBRExpression"/>", "melding": "De was-ID verwijzing ontbreekt in GIO <sch:value-of select="geo:FRBRExpression"/>. Het GIO bevat GIO-wijzigingen waardoor een was-ID verwijzing verplicht is. Voeg de was-ID toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_gml_03090">
      <sch:title>Geen optionele gml AbstractFeatureType elementen in de geo: namespace</sch:title>
      <sch:rule context="gml:metaDataProperty[parent::geo:*] | gml:description[parent::geo:*] | gml:descriptionReference[parent::geo:*] | gml:identifier[parent::geo:*] | gml:name[parent::geo:*] | gml:boundedBy[parent::geo:*] | gml:location[parent::geo:*] | gml:PriorityLocation[parent::geo:*]">
         <sch:let name="kenmerk">
            <xsl:if test="name(..) = 'geo:GeoInformatieObjectVaststelling' or name(..) = 'geo:GeoInformatieObjectVersie' or name(..) = 'geo:GeoInformatieObjectMutatie'"> binnen GIO met FRBRExpressie '<xsl:value-of select="../descendant::geo:FRBRExpression"/>'</xsl:if>
            <xsl:if test="name(..) = 'geo:Locatie'"> met naam '<xsl:value-of select="../geo:naam"/>'</xsl:if>
            <xsl:if test="name(..) = 'geo:LocatieMutatie'"> met naam '<xsl:value-of select="../geo:naam"/>'</xsl:if>
            <xsl:if test="name(..) = 'geo:Gebied'"> met label '<xsl:value-of select="../geo:label"/>'</xsl:if>
         </sch:let>
         <sch:report id="STOP3090" test="." role="fout">
				{"code": "STOP3090", "Kenmerk": "<sch:value-of select="$kenmerk"/>", "Element": "<sch:value-of select="string(node-name(.))"/>", "Parent": "<sch:value-of select="string(node-name(..))"/>", "melding": "<sch:value-of select="string(node-name(..))"/>
            <sch:value-of select="$kenmerk"/> bevat het optionele gml-element <sch:value-of select="string(node-name(.))"/>. Dit element mag niet worden gebruikt in een GIO. Verwijder dit element.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
</sch:schema>
