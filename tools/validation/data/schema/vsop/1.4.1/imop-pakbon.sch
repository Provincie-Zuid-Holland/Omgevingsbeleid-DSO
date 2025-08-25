<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="data" uri="https://standaarden.overheid.nl/stop/imop/data/"/>
   <sch:ns prefix="cons"
           uri="https://standaarden.overheid.nl/stop/imop/consolidatie/"/>
   <sch:ns prefix="uws"
           uri="https://standaarden.overheid.nl/stop/imop/uitwisseling/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validaties van pakbon</sch:p>
   <sch:let name="nst" value="'https://standaarden.overheid.nl/stop/imop/tekst/'"/>
   <sch:let name="nsd" value="'https://standaarden.overheid.nl/stop/imop/data/'"/>
   <sch:let name="nsg" value="'https://standaarden.overheid.nl/stop/imop/geo/'"/>
   <sch:let name="nsc"
            value="'https://standaarden.overheid.nl/stop/imop/consolidatie/'"/>
   <sch:pattern id="sch_uws_001">
      <sch:title>IMOP-schemaversies in component gelijk</sch:title>
      <sch:rule context="uws:Component" id="STOP1200">
         <sch:let name="imop-modules"
                  value="uws:heeftModule/uws:Module[starts-with(uws:namespace,'https://standaarden.overheid.nl/stop/imop/')]"/>
         <sch:let name="eersteversie" value="$imop-modules[1]/uws:schemaversie"/>
         <sch:assert test="every $v in $imop-modules/uws:schemaversie satisfies $v=$eersteversie"
                     role="fout">
        {"code": "STOP1200", "Work-id": "<sch:value-of select="uws:FRBRWork"/>", "melding": "De IMOP-modules binnen de Component met FRBRWork <sch:value-of select="uws:FRBRWork"/> hebben niet allemaal dezelfde IMOP-schemaversie.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_uws_002">
      <sch:title>een juridische regeltekst MOET samen met een RegelingVersieMetadata-module in component</sch:title>
      <sch:let name="regelingtypes"
               value="'RegelingCompact', 'RegelingKlassiek', 'RegelingVrijetekst', 'RegelingTijdelijkdeel'"/>
      <sch:rule context="uws:Component[uws:heeftModule/uws:Module[uws:namespace=$nst][normalize-space(uws:localName)=$regelingtypes]]"
                id="STOP1204">
         <sch:assert test="uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='RegelingVersieMetadata']"
                     role="waarschuwing">
        {"code": "STOP1204", "Work-id": "<sch:value-of select="uws:FRBRWork"/>", "melding": "De component <sch:value-of select="uws:FRBRWork"/> heeft wel een module met juridische tekst maar geen RegelingVersieMetadata-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_uws_003">
      <sch:title>informatieobject MOET samen met een IO-VersieMetadata-module in component</sch:title>
      <sch:let name="iotypes"
               value="'GeoInformatieObjectVaststelling', 'GeoInformatieObjectVersie'"/>
      <sch:rule context="uws:Component [uws:heeftModule/uws:Module[uws:namespace=$nsg][normalize-space(uws:localName)=$iotypes]]"
                id="STOP1205">
         <sch:assert test="uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='InformatieObjectVersieMetadata']"
                     role="waarschuwing">
        {"code": "STOP1205", "Work-id": "<sch:value-of select="uws:FRBRWork"/>", "melding": "De component <sch:value-of select="uws:FRBRWork"/> heeft wel een module met een informatieobject maar heeft geen InformatieObjectVersieMetadata-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_uws_004">
      <sch:title>Component in een pakbon heeft id-module tenzij soortWork = 024 (versieinformatie) </sch:title>
      <sch:rule context="uws:Component" id="STOP1208">
         <sch:let name="SWversieinformatie" value="'/join/id/stop/work_024'"/>
         <sch:let name="soortWork"
                  value="descendant::uws:soortWork/normalize-space(string())"/>
         <sch:assert test="$soortWork=$SWversieinformatie or (uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='ExpressionIdentificatie']         |uws:heeftModule/uws:Module[uws:namespace=$nsc][normalize-space(uws:localName)='ConsolidatieIdentificatie'])"
                     role="waarschuwing">
        {"code": "STOP1208", "Work-id": "<sch:value-of select="uws:FRBRWork"/>", "melding": "De Component met <sch:value-of select="uws:FRBRWork"/> heeft geen ExpressionIdentificatie- of ConsolidatieIdentificatie-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},</sch:assert>
      </sch:rule>
   </sch:pattern>
</sch:schema>
