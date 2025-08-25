<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="data" uri="https://standaarden.overheid.nl/stop/imop/data/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validatie voor metadata</sch:p>
   <sch:pattern id="sch_data_004">
      <sch:title>OfficieleTitel InformatieObject is JOIN identifier</sch:title>
      <sch:rule context="data:InformatieObjectMetadata">
         <sch:p>De officieleTitel van een InformatieObject MOET starten met /join/id/</sch:p>
         <sch:assert id="STOP1015"
                     test="starts-with(./data:officieleTitel/string(), '/join/id/')"
                     role="fout"> {"code": "STOP1015", "substring": "<sch:value-of select="./data:officieleTitel"/>", "melding": "De waarde van officieleTitel <sch:value-of select="./data:officieleTitel"/> MOET starten met /join/id/. Maak er een JOIN-identifier van.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_005">
      <sch:title>Toegestane type informatieobjecten icm publicatie instructie</sch:title>
      <sch:rule context="data:InformatieObjectMetadata">
         <sch:let name="formaat"
                  value="normalize-space(xs:string(data:formaatInformatieobject))"/>
         <sch:let name="is_GIO" value="$formaat='/join/id/stop/informatieobject/gio_002'"/>
         <sch:let name="is_PDF" value="$formaat='/join/id/stop/informatieobject/doc_001'"/>
         <sch:p> GIO's alleen bekend te maken of informatief zijn NIET TOEGESTAAN zolang deze niet expliciet benoemd 
        zijn in een TPOD</sch:p>
         <sch:report id="STOP1073"
                     test="$is_GIO and (normalize-space(xs:string(data:publicatieinstructie)) = 'Informatief' or normalize-space(xs:string(data:publicatieinstructie)) = 'AlleenBekendTeMaken') "
                     role="fout">
        {"code": "STOP1073", "officieleTitel": "<sch:value-of select="data:officieleTitel"/>", "formaat": "<sch:value-of select="$formaat"/>", "type": "<sch:value-of select="data:publicatieinstructie"/>", "melding": "Een informatieobject <sch:value-of select="data:officieleTitel"/> met formaat <sch:value-of select="$formaat"/> en publicatieinstructie <sch:value-of select="data:publicatieinstructie"/> is niet toegestaan, hiervoor ontbreekt een TPOD instructie.", "ernst": "fout"},</sch:report>
         <sch:p>PDF's informatief zijn NIET TOEGESTAAN zolang deze niet expliciet benoemd zijn in een TPOD</sch:p>
         <sch:report id="STOP1074"
                     test="$is_PDF and normalize-space(xs:string(data:publicatieinstructie)) = 'Informatief' "
                     role="fout">
        {"code": "STOP1074", "officieleTitel": "<sch:value-of select="data:officieleTitel"/>", "formaat": "<sch:value-of select="$formaat"/>", "type": "<sch:value-of select="data:publicatieinstructie"/>", "melding": "Een informatieobject <sch:value-of select="data:officieleTitel"/> met formaat <sch:value-of select="$formaat"/> en publicatieinstructie <sch:value-of select="data:publicatieinstructie"/> is niet toegestaan, hiervoor ontbreekt een TPOD instructie.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_006">
      <sch:title>RegelingVersieMetadata validaties</sch:title>
      <sch:rule context="data:RegelingVersieMetadata/data:versienummer">
         <sch:p>Versienummer van regeling moet voldoen onze specificaties</sch:p>
         <sch:report id="STOP1016"
                     test="not(matches(./string(), '^[a-zA-Z0-9\-]{1,32}$'))"
                     role="fout"> {"code": "STOP1016", "substring": "<sch:value-of select="./string()"/>", "melding": "Het versienummer van een regeling <sch:value-of select="./string()"/> MOET bestaan uit maximaal 32 cijfers, onderkast- en bovenkast-letters en -, en MAG NIET bestaan uit punt en underscore.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_007">
      <sch:title>informatieobjectRefs uniek</sch:title>
      <sch:rule context="data:informatieobjectRefs">
         <sch:p>alle data:informatieobjectref binnen een data:informatieobjectRefs zijn uniek</sch:p>
         <sch:report id="STOP1018"
                     test="count(./data:informatieobjectRef) != count(distinct-values(./data:informatieobjectRef))"
                     role="fout"> {"code": "STOP1018", "melding": "Alle referenties binnen informatieobjectRefs moeten uniek zijn. Pas dit aan.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_008"
                see="data:rechtsgebieden data:overheidsdomeinen data:onderwerpen     data:alternatieveTitels data:opvolging">
      <sch:title>data:rechtsgebieden, data:overheidsdomeinen, data:onderwerpen,
      data:alternatieveTitels, data:opvolging uniek</sch:title>
      <sch:rule context="data:rechtsgebieden">
         <sch:p>data:rechtsgebieden zijn uniek</sch:p>
         <sch:report id="STOP1019"
                     test="count(./data:rechtsgebied) != count(distinct-values(./data:rechtsgebied))"
                     role="fout"> {"code": "STOP1019", "melding": "Gebruik elke waarde binnen container data:rechtsgebieden maar één keer.", "ernst": "fout"},</sch:report>
      </sch:rule>
      <sch:rule context="data:overheidsdomeinen">
         <sch:p>data:overheidsdomeinen zijn uniek</sch:p>
         <sch:report id="STOP1030"
                     test="count(./data:overheidsdomein) != count(distinct-values(./data:overheidsdomein))"
                     role="fout">
        {"code": "STOP1030", "melding": "Gebruik elke waarde binnen container data:overheidsdomeinen maar één keer.", "ernst": "fout"},</sch:report>
      </sch:rule>
      <sch:rule context="data:onderwerpen">
         <sch:p>data:onderwerpen zijn uniek</sch:p>
         <sch:report id="STOP1031"
                     test="count(./data:onderwerp) != count(distinct-values(./data:onderwerp))"
                     role="fout"> {"code": "STOP1031", "melding": "Gebruik elke waarde binnen container data:onderwerpen maar één keer.", "ernst": "fout"},</sch:report>
      </sch:rule>
      <sch:rule context="data:alternatieveTitels">
         <sch:p>data:alternatieveTitels zijn uniek</sch:p>
         <sch:report id="STOP1022"
                     test="count(./data:alternatieveTitel) != count(distinct-values(./data:alternatieveTitel))"
                     role="fout">
        {"code": "STOP1022", "melding": "De alternatieve titels binnen alternatieveTitels MOETEN allen uniek zijn.", "ernst": "fout"},</sch:report>
      </sch:rule>
      <sch:rule context="data:opvolging">
         <sch:p>data:opvolging zijn uniek</sch:p>
         <sch:report id="STOP1023"
                     test="count(./data:opvolgerVan) != count(distinct-values(./data:opvolgerVan))"
                     role="fout"> {"code": "STOP1023", "melding": "Alle opvolgerVan binnen een opvolging MOETEN uniek zijn.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_009">
      <sch:title>alternatieveTitel niet gelijk aan citeertitel</sch:title>
      <sch:rule context="data:alternatieveTitel">
         <sch:p>Geen van de alternatieveTitel is gelijk aan de citeertitel</sch:p>
         <sch:report id="STOP1020"
                     test="./string() = ../../data:heeftCiteertitelInformatie/data:CiteertitelInformatie/data:citeertitel/string()"
                     role="fout"> {"code": "STOP1020", "melding": "De citeertitel MAG NIET gelijk zijn aan een alternatieve titel.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_010">
      <sch:title>data:opvolgerVan wijst naar een Work van een Regeling of informatieobject</sch:title>
      <sch:rule context="data:opvolgerVan">
         <sch:p>data:opvolgerVan wijst naar een Work van een Regeling of informatieobject</sch:p>
         <sch:assert id="STOP1024"
                     test="matches(./string(), '^/akn/(nl|aw|cw|sx)/act|^/join/id/regdata/')"
                     role="fout">
        {"code": "STOP1024", "substring": "<sch:value-of select="./string()"/>", "melding": "In opvolgerVan (<sch:value-of select="./string()"/>) wordt niet verwezen naar een work van een Regeling of Informatieobject ('/AKN/act/...' of '/join/id/regdata/...'). Corrigeer de verwijzing opvolgerVan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_011">
      <sch:title>data:uri moet corresponderen met data:soortRef</sch:title>
      <sch:rule context="data:TekstReferentie">
         <sch:let name="is_akn" value="./data:soortRef/string() = 'AKN'"/>
         <sch:let name="is_jci" value="./data:soortRef/string() = 'JCI'"/>
         <sch:let name="is_url" value="./data:soortRef/string() = 'URL'"/>
         <sch:let name="akn_patroon" value="'^/akn/(nl|aw|cw|sx)/act'"/>
         <sch:let name="jci_patroon" value="'^jci'"/>
         <sch:let name="url_patroon" value="'^http[s]?://'"/>
         <sch:p>Het patroon in data:uri moet overeenkomen met zijn data:soortRef (URL: correcte
        http-ref, AKN: correcte AKN, JCI: correcte JCI)</sch:p>
         <sch:assert id="STOP1021"
                     test="($is_akn and matches(./data:uri/string(), $akn_patroon)) or ($is_jci and matches(./data:uri/string(), $jci_patroon)) or ($is_url and matches(./data:uri/string(), $url_patroon))"
                     role="fout"> {"code": "STOP1021", "substring": "<sch:value-of select="./data:uri/string()"/>", "melding": "De uri <sch:value-of select="./data:uri/string()"/> MOET corresponderen met de soortRef. Pas deze aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!-- STOP1032/STOP1033 verwijderd: fouten in OfficielePublicatieMetadata kunnen niet door BG hersteld worden en moeten eerder afgevangen worden -->
   <sch:pattern id="sch_data_013">
      <sch:title>soortBestuursorgaan gevuld voor decentraal</sch:title>
      <sch:let name="is_decentraal" value="'gemeente|provincie|waterschap'"/>
      <sch:rule context="data:RegelingMetadata[data:eindverantwoordelijke[matches(., $is_decentraal)]] | data:BesluitMetadata[data:eindverantwoordelijke[matches(., $is_decentraal)]]">
         <sch:report id="STOP1034"
                     test="not(data:soortBestuursorgaan) or data:soortBestuursorgaan = ''"
                     role="fout">{"code": "STOP1034", "melding": "soortBestuursorgaan MAG NIET leeg zijn voor gemeente, provincie of waterschap. Vul soortBestuursorgaan in.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_014">
      <sch:title>soortBestuursorgaan passend bij eindverantwoordelijke</sch:title>
      <sch:rule context="data:RegelingMetadata | data:BesluitMetadata">
         <sch:let name="is_gemeente"
                  value="matches(./data:eindverantwoordelijke, 'gemeente')"/>
         <sch:let name="is_waterschap"
                  value="matches(./data:eindverantwoordelijke, 'waterschap')"/>
         <sch:let name="is_provincie"
                  value="matches(./data:eindverantwoordelijke, 'provincie')"/>
         <sch:let name="is_staat"
                  value="matches(./data:eindverantwoordelijke, 'ministerie')"/>
         <sch:let name="gemeente_bestuursorgaan_patroon"
                  value="'c_2c4e7407|c_28ecfd6d|c_2a7d8663|^$'"/>
         <sch:let name="waterschap_bestuursorgaan_patroon"
                  value="'c_70c87e3d|c_5cc92c89|c_f70a6113|^$'"/>
         <sch:let name="provincie_bestuursorgaan_patroon"
                  value="'c_e24d39f6|c_61676cbc|c_411b4e4a|^$'"/>
         <sch:let name="staat_bestuursorgaan_patroon"
                  value="'c_bcfb7b4e|c_91fb5e42|c_3aaa4d12|^$'"/>
         <sch:assert id="STOP1035"
                     test="($is_gemeente and matches(./data:soortBestuursorgaan, $gemeente_bestuursorgaan_patroon)) or ($is_waterschap and matches(./data:soortBestuursorgaan, $waterschap_bestuursorgaan_patroon)) or ($is_provincie and matches(./data:soortBestuursorgaan, $provincie_bestuursorgaan_patroon)) or ($is_staat and matches(./data:soortBestuursorgaan, $staat_bestuursorgaan_patroon)) or (not(./data:eindverantwoordelijke))"
                     role="fout">{"code": "STOP1035", "melding": "soortBestuursorgaan MOET corresponderen met eindverantwoordelijke. Pas soortBestuursorgaan of eindverantwoordelijke aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_015">
      <sch:rule context="*:heeftGeboorteregeling">
         <sch:p>Een AKN identificatie in een geboorteregeling MOET starten met /akn/nl/act </sch:p>
         <sch:assert id="STOP1060"
                     test="starts-with(./normalize-space(), '/akn/nl/act')"
                     role="fout">
        {"code": "STOP1060", "Work": "<sch:value-of select="."/>", "melding": "heeftGeboorteregeling verwijst naar <sch:value-of select="."/>. Dit is geen work van een Regeling ('/AKN/nl/act/...'). Corrigeer de verwijzing heeftGeboorteregeling.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!-- STOP1075 vervallen -->
   <!-- STOP1083 vervallen -->
   <!-- STOP1085 vervallen -->
   <sch:pattern id="sch_data_2082">
      <sch:rule context="data:soortRegeling">
         <sch:p>Het gebruik van "Voorbeschermingsregels" als <codeph>soortRegeling</codeph> wordt ontraden. 
        Aangeraden wordt de specifiekere "Voorbeschermingsregels Omgevingsplan" (regelingtype_015) 
        of "Voorbeschermingsregels Omgevingsverordening" (regelingtype_016) te gebruiken.</sch:p>
         <sch:let name="voorbeschermingsregels"
                  value="'^/join/id/stop/regelingtype_009$'"/>
         <sch:report id="STOP2082"
                     test="matches(./string(),$voorbeschermingsregels)"
                     role="ontraden">
        {"code": "STOP2082", "soortRegeling": "<sch:value-of select="."/>", "melding": "Gebruik van de waarde <sch:value-of select="."/> voor soortRegeling wordt ontraden. Gebruik de specifiekere waarden \"Voorbeschermingsregels Omgevingsplan\" of \"Voorbeschermingsregels Omgevingsverordening\".", "ernst": "ontraden"},</sch:report>
      </sch:rule>
   </sch:pattern>
</sch:schema>
