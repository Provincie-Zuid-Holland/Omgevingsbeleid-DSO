<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="data" uri="https://standaarden.overheid.nl/stop/imop/data/"/>
   <sch:ns prefix="tekst" uri="https://standaarden.overheid.nl/stop/imop/tekst/"/>
   <sch:ns prefix="geo" uri="https://standaarden.overheid.nl/stop/imop/geo/"/>
   <sch:ns prefix="gio" uri="https://standaarden.overheid.nl/stop/imop/gio/"/>
   <sch:ns prefix="cons"
           uri="https://standaarden.overheid.nl/stop/imop/consolidatie/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validatie van de regels voor AKNs en JOINs</sch:p>
   <sch:pattern id="sch_data_001">
      <sch:title>Generieke AKN en JOIN validaties</sch:title>
      <sch:rule context="*:FRBRWork | *:FRBRExpression | *:instrumentVersie | *:instrument | *:doel | tekst:ExtIoRef | data:opvolgerVan | data:heeftGeboorteregeling | data:informatieobjectRef | data:mededelingOver | cons:publiceert | data:publiceert | gio:contextGIOs | geo:wasID | cons:heeftTijdelijkDeel | tekst:ExtRef[@soort = 'AKN'][matches(@ref, '^/akn/(nl|aw|cw|sx)/')] | tekst:ExtRef[@soort = 'JOIN']">
         <sch:let name="taalexpressie" value="'^(nld|eng|fry|pap|mul|und)$'"/>
         <sch:let name="landexpressie" value="'^(nl|aw|cw|sx)$'"/>
         <sch:let name="AKNexpressie" value="'^(bill|act|doc|officialGazette)$'"/>
         <sch:let name="JOINexpressie"
                  value="'^(pubdata|regdata|infodata|proces|versie)$'"/>
         <sch:let name="Consolidatieexpressie"
                  value="'^(land|provincie|gemeente|waterschap|consolidatie)$'"/>
         <sch:let name="BGexpressie"
                  value="'^(mnre\d{4}|mn\d{3}|gm\d{4}|ws\d{4}|pv\d{2})$'"/>
         <sch:let name="Identificatie">
            <xsl:choose>
               <xsl:when test="string(local-name(.)) = 'ExtRef'">
            <!-- AKN staat achtervoegsels toe bij verwijzingen, deze niet valideren -->
                  <xsl:choose>
                     <xsl:when test="contains(@ref, '/!')">
                        <xsl:value-of select="substring-before(normalize-space(@ref), '/!')"/>
                     </xsl:when>
                     <xsl:when test="contains(@ref, '/~')">
                        <xsl:value-of select="substring-before(normalize-space(@ref), '/~')"/>
                     </xsl:when>
                     <xsl:when test="contains(@ref, '#')">
                        <xsl:value-of select="substring-before(normalize-space(@ref), '#')"/>
                     </xsl:when>
                     <xsl:otherwise>
                        <xsl:value-of select="normalize-space(@ref)"/>
                     </xsl:otherwise>
                  </xsl:choose>
               </xsl:when>
               <xsl:otherwise>
                  <xsl:value-of select="normalize-space(./string())"/>
               </xsl:otherwise>
            </xsl:choose>
         </sch:let>
         <sch:let name="Identificatie_reeks" value="tokenize($Identificatie, '/')"/>
         <sch:let name="Identificatie_deel1" value="$Identificatie_reeks[2]"/>
         <sch:let name="isAKN" value="starts-with($Identificatie, '/akn/')"/>
         <sch:let name="isJOIN" value="starts-with($Identificatie, '/join/')"/>
         <sch:let name="Identificatie_deel2" value="$Identificatie_reeks[3]"/>
         <sch:let name="Identificatie_deel3" value="$Identificatie_reeks[4]"/>
         <sch:let name="IsPublicatie" value="$Identificatie_deel3 = 'officialGazette'"/>
         <sch:let name="IsDoel" value="$Identificatie_deel3 = 'proces'"/>
         <sch:let name="IsAct" value="$Identificatie_deel3 = 'act'"/>
         <sch:let name="AKNValide" value="matches($Identificatie_deel3, $AKNexpressie)"/>
         <sch:let name="JOINValide" value="matches($Identificatie_deel3, $JOINexpressie)"/>
         <sch:let name="Identificatie_deel4" value="$Identificatie_reeks[5]"/>
         <sch:let name="IsConsolidatie"
                  value="matches($Identificatie_deel4, $Consolidatieexpressie)"/>
         <sch:let name="IsBRPcode" value="matches($Identificatie_deel4, $BGexpressie)"/>
         <sch:let name="Identificatie_deel5" value="$Identificatie_reeks[6]"/>
         <sch:let name="Identificatie_deel6" value="$Identificatie_reeks[7]"/>
         <sch:let name="Identificatie_deel7" value="$Identificatie_reeks[8]"/>
         <sch:let name="Identificatie_rest"
                  value="substring-after($Identificatie, concat($Identificatie_deel6, '/', $Identificatie_deel7))"/>
         <sch:let name="IsExpressie"
                  value="exists($Identificatie_deel7) and contains($Identificatie_deel7, '@')"/>
         <sch:let name="Expressie_datum">
            <xsl:choose>
               <xsl:when test="contains($Identificatie_deel7, ';')">
                  <xsl:value-of select="substring-before(substring-after($Identificatie_deel7, '@'), ';')"/>
               </xsl:when>
               <xsl:otherwise>
                  <xsl:value-of select="substring-after($Identificatie_deel7, '@')"/>
               </xsl:otherwise>
            </xsl:choose>
         </sch:let>
         <sch:p>Een AKN- of JOIN-identificatie mag geen punt bevatten</sch:p>
         <sch:report id="STOP1000" test="contains($Identificatie, '.')" role="fout">
        {"code": "STOP1000", "ID": "<sch:value-of select="$Identificatie"/>", "melding": "De identifier <sch:value-of select="$Identificatie"/> bevat een punt. Dit is niet toegestaan. Verwijder de punt.", "ernst": "fout"},</sch:report>
         <sch:p>Een AKN of JOIN identificatie MOET starten met /akn/ of /join/</sch:p>
         <sch:assert id="STOP1014" test="$isAKN or $isJOIN" role="fout">
        {"code": "STOP1014", "ID": "<sch:value-of select="$Identificatie"/>", "melding": "De waarde <sch:value-of select="$Identificatie"/> begint niet met /akn/ of /join/. Pas de waarde aan.", "ernst": "fout"},</sch:assert>
         <sch:p>AKN-identificatie MOET als tweede deel een geldig land hebben (behalve ExtRef
        soort=AKN, die wordt alleen gevalideert als begint met /akn/nl)</sch:p>
         <sch:report id="STOP1002"
                     test="$isAKN and not(matches($Identificatie_deel2, $landexpressie))"
                     role="fout">
	    {"code": "STOP1002", "Work-ID": "<sch:value-of select="$Identificatie"/>", "substring": "<sch:value-of select="$Identificatie_deel2"/>", "melding": "Landcode <sch:value-of select="$Identificatie_deel2"/> in de AKN-identificatie <sch:value-of select="$Identificatie"/> is niet toegestaan. Pas landcode aan.", "ernst": "fout"},</sch:report>
         <sch:p>JOIN-identificatie MOET als tweede deel een geldig objecttype hebben</sch:p>
         <sch:report id="STOP1003"
                     test="$isJOIN and not(matches($Identificatie_deel2, '^(id)$'))"
                     role="fout">
	    {"code": "STOP1003", "Work-ID": "<sch:value-of select="$Identificatie"/>", "melding": "Tweede deel JOIN-identificatie <sch:value-of select="$Identificatie"/> moet gelijk zijn aan 'id'. Pas dit aan.", "ernst": "fout"},</sch:report>
         <sch:p>JOIN-identificatie MOET als derde deel regdata, pubdata, infodata of proces
        hebben</sch:p>
         <sch:report id="STOP1004" test="$isJOIN and not($JOINValide)" role="fout">
	  	{"code": "STOP1004", "Work-ID": "<sch:value-of select="$Identificatie"/>", "melding": "Derde deel JOIN-identificatie <sch:value-of select="$Identificatie"/> moet gelijk zijn aan 'regdata', 'pubdata', 'infodata' voor verwijzing naar een informatieobject of 'proces' voor een doel. Pas dit aan.", "ernst": "fout"},</sch:report>
         <sch:p>AKN-identificatie MOET als derde deel bill, act, doc of officialGazette hebben</sch:p>
         <sch:report id="STOP2081" test="$isAKN and not($AKNValide)" role="fout">
	  	{"code": "STOP2081", "Work-ID": "<sch:value-of select="$Identificatie"/>", "melding": "Derde deel AKN-identificatie <sch:value-of select="$Identificatie"/> moet gelijk zijn aan 'bill', 'act', 'doc' voor verwijzing naar een besluit, regeling, overige te publiceren documenten of 'officialGazette' voor een gepubliceerd document. Pas dit aan.", "ernst": "fout"},</sch:report>
         <sch:p>Vierde deel AKN/JOIN m.u.v. offpub MOET brp-code of code voor geconsolideerde regeling
        zijn.</sch:p>
         <sch:report id="STOP1010"
                     test="($AKNValide or $JOINValide) and not($IsPublicatie or $IsBRPcode or $IsConsolidatie)"
                     role="fout">
		  {"code": "STOP1010", "Work-ID": "<sch:value-of select="$Identificatie"/>", "substring": "<sch:value-of select="$Identificatie_deel4"/>", "melding": "Vierde deel van AKN/JOIN (<sch:value-of select="$Identificatie"/>) moet gelijk zijn aan een brp-code, een code voor geconsolidatieolideerde instrumenten of 'proces' voor een doel. Pas (<sch:value-of select="$Identificatie_deel4"/>) aan.", "ernst": "fout"},</sch:report>
         <sch:p>AKN of JOIN identificatie MOET als vijfde deel jaartal of geldigde datum hebben</sch:p>
         <sch:assert id="STOP1006"
                     test="($Identificatie_deel5 castable as xs:date and string-length($Identificatie_deel5) = 10) or ($Identificatie_deel5 castable as xs:gYear and string-length($Identificatie_deel5) = 4)"
                     role="fout">
		  {"code": "STOP1006", "Work-ID": "<sch:value-of select="$Identificatie"/>", "melding": "Vijfde deel AKN- of JOIN-identificatie <sch:value-of select="$Identificatie"/> moet gelijk zijn aan jaartal of geldige datum. Pas dit aan.", "ernst": "fout"},</sch:assert>
         <sch:p>AKN of JOIN Work-identificatie MOET zes delen hebben gescheiden door /</sch:p>
         <sch:report id="STOP2078"
                     test="not($IsExpressie) and ($Identificatie_deel7 != '' or $Identificatie_rest != '')"
                     role="fout">
		  {"code": "STOP2078", "Work-ID": "<sch:value-of select="$Identificatie"/>", "melding": "De identifier <sch:value-of select="$Identificatie"/> bestaat niet uit minimaal zes door een '/' gescheiden delen. Dit is niet toegestaan. Geef de identifier het correcte formaat.", "ernst": "fout"},</sch:report>
         <sch:p>AKN of JOIN identificatie MOET als zesde deel een overig-aanduiding hebben beginnend
        met letter of cijfer van maximaal 128 tekens lang en bestaande uit letters, cijfers, _ of
        -</sch:p>
         <sch:assert id="STOP2079"
                     test="matches($Identificatie_deel6, '^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$')"
                     role="fout">
		  {"code": "STOP2079", "Work-ID": "<sch:value-of select="$Identificatie"/>", "substring": "<sch:value-of select="$Identificatie_deel6"/>", "melding": "De identifier <sch:value-of select="$Identificatie"/> heeft geen correcte 'overig'-aanduiding <sch:value-of select="$Identificatie_deel6"/>. Dit deel begint niet met een letter of cijfer en/of bevat ook andere tekens dan letters, cijfers, '_' en '-'. Corrigeer de identifier.", "ernst": "fout"},</sch:assert>
         <sch:p>AKN of JOIN Expressie-identificatie MOET zeven delen hebben gescheiden door / met in
        het zevende deel een @.</sch:p>
         <sch:report id="STOP2080"
                     test="$IsExpressie and $Identificatie_rest != ''"
                     role="fout">
		  {"code": "STOP2080", "Expression-ID": "<sch:value-of select="$Identificatie"/>", "TeLang": "<sch:value-of select="$Identificatie_rest"/>", "melding": "De expressie-identifier <sch:value-of select="$Identificatie"/> bestaat uit meer dan zeven delen gescheiden door een '/'. <sch:value-of select="$Identificatie_rest"/> is overbodig. Corrigeer de expressie-identifier.", "ernst": "fout"},</sch:report>
         <sch:p>AKN- of JOIN-identificatie (expressie) MOET als deel voorafgaand aan de '@' een geldige
        taal hebben</sch:p>
         <sch:assert id="STOP1009"
                     test="not($IsExpressie) or matches(substring-before($Identificatie_deel7, '@'), $taalexpressie)"
                     role="fout">
		  {"code": "STOP1009", "Expression-ID": "<sch:value-of select="$Identificatie"/>", "substring": "<sch:value-of select="substring-before($Identificatie_deel7, '@')"/>", "melding": "Voor een AKN- of JOIN-identificatie (<sch:value-of select="$Identificatie"/>) moet het deel voorafgaand aan de '@' (<sch:value-of select="substring-before($Identificatie_deel7, '@')"/>) een geldige taal zijn ('nld','eng','fry','pap','mul','und'). Pas dit aan.", "ernst": "fout"},</sch:assert>
         <sch:p>Een identificatie (expressie) MOET als eerste deel na de '@' een jaartal of een geldige
        datum hebben TENZIJ het een niet-geconsolideerde regeling is.</sch:p>
         <sch:report id="STOP1007"
                     test="$IsExpressie and (not($IsAct) or $IsConsolidatie) and not(($Expressie_datum castable as xs:date and (string-length($Expressie_datum) = 10)) or ($Expressie_datum castable as xs:gYear and (string-length($Expressie_datum) = 4)))"
                     role="fout">
		  {"code": "STOP1007", "Expression-ID": "<sch:value-of select="$Identificatie"/>", "melding": "Voor een AKN- of JOIN-identificatie (<sch:value-of select="$Identificatie"/>) moet het eerste deel na de '@' een jaartal of een geldige datum zijn. Pas dit aan.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_002">
      <sch:title>ExpressionID begint met WorkID</sch:title>
      <sch:rule context="*:ExpressionIdentificatie | geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie">
         <sch:let name="Work" value="normalize-space(*:FRBRWork)"/>
         <sch:let name="Expression" value="normalize-space(*:FRBRExpression)"/>
         <sch:p>Het deel vóór de @ van de FRBRExpression moet gelijk aan zijn FRBRWork</sch:p>
         <sch:assert id="STOP1001"
                     test="starts-with($Expression, concat($Work, '/'))"
                     role="fout">
        {"code": "STOP1001", "Work-ID": "<sch:value-of select="$Work"/>", "Expression-ID": "<sch:value-of select="$Expression"/>", "melding": "Het gedeelte van de FRBRExpression <sch:value-of select="$Expression"/> vóór de 'taalcode/@' is niet gelijk aan de FRBRWork-identificatie <sch:value-of select="$Work"/>.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_005">
      <sch:title>AKN/JOIN validaties Expression/Work icm soortWork in
      ExpressionIdentificatie</sch:title>
      <sch:rule context="*:ExpressionIdentificatie">
         <sch:let name="soortWork" value="normalize-space(./*:soortWork/string())"/>
         <sch:let name="Expression" value="normalize-space(./*:FRBRExpression/string())"/>
         <sch:let name="Work" value="normalize-space(./*:FRBRWork/string())"/>
         <sch:let name="Expression_reeks" value="tokenize($Expression, '/')"/>
         <sch:let name="Expression_datum_work" value="$Expression_reeks[6]"/>
         <sch:let name="Expression_restdeel" value="$Expression_reeks[8]"/>
         <sch:let name="Expression_restdeel_reeks"
                  value="tokenize($Expression_restdeel, '@')"/>
         <sch:let name="Expression_restdeel_deel2" value="$Expression_restdeel_reeks[2]"/>
         <sch:let name="Expression_restdeel_deel2_reeks"
                  value="tokenize($Expression_restdeel_deel2, ';')"/>
         <sch:let name="Expression_datum_expr"
                  value="$Expression_restdeel_deel2_reeks[1]"/>
         <sch:let name="Work_reeks" value="tokenize($Work, '/')"/>
         <sch:let name="Work_objecttype" value="$Work_reeks[3]"/>
         <sch:let name="Work_collectie" value="$Work_reeks[4]"/>
         <sch:let name="Work_documenttype" value="$Work_reeks[4]"/>
         <sch:let name="Work_overheid" value="$Work_reeks[5]"/>
         <sch:let name="is_besluit" value="$soortWork = '/join/id/stop/work_003'"/>
         <sch:let name="is_kennisgeving" value="$soortWork = '/join/id/stop/work_023'"/>
         <sch:let name="is_mededeling" value="$soortWork = '/join/id/stop/work_025'"/>
         <sch:let name="is_rectificatie" value="$soortWork = '/join/id/stop/work_018'"/>
         <sch:let name="is_tijdelijkregelingdeel"
                  value="$soortWork = '/join/id/stop/work_021'"/>
         <sch:let name="is_regeling"
                  value="$soortWork = '/join/id/stop/work_019' or $soortWork = '/join/id/stop/work_006' or $soortWork = '/join/id/stop/work_021' or $soortWork = '/join/id/stop/work_022'"/>
         <sch:let name="is_publicatie" value="$soortWork = '/join/id/stop/work_015'"/>
         <sch:let name="is_informatieobject"
                  value="$soortWork = '/join/id/stop/work_010'"/>
         <sch:let name="is_cons_informatieobject"
                  value="$soortWork = '/join/id/stop/work_005'"/>
         <sch:let name="bladcode" value="'^(bgr|gmb|prb|stb|stcrt|trb|wsb)$'"/>
         <sch:let name="is_join" value="$is_informatieobject"/>
         <sch:let name="is_akn"
                  value="$is_besluit or $is_publicatie or $is_regeling or $is_kennisgeving or $is_rectificatie or $is_mededeling"/>
         <sch:p>AKN-identificatie (Work) van officiele publicatie MOET als derde deel officialGazette
        hebben</sch:p>
         <sch:report id="STOP1011"
                     test="$is_publicatie and not(matches($Work_documenttype, '^officialGazette$'))"
                     role="fout">
	    {"code": "STOP1011", "Work-ID": "<sch:value-of select="$Work"/>", "substring": "<sch:value-of select="$Work_documenttype"/>", "melding": "Derde veld <sch:value-of select="$Work_documenttype"/> in de AKN-identificatie <sch:value-of select="$Work"/> is niet toegestaan bij officiele publicatie. Pas dit veld aan.", "ernst": "fout"},</sch:report>
         <sch:p>AKN-identificatie (Work) van besluit MOET als derde deel bill hebben</sch:p>
         <sch:report id="STOP1013"
                     test="$is_besluit and not(matches($Work_documenttype, '^bill$'))"
                     role="fout">
	    {"code": "STOP1013", "Work-ID": "<sch:value-of select="$Work"/>", "substring": "<sch:value-of select="$Work_documenttype"/>", "melding": "Derde veld <sch:value-of select="$Work_documenttype"/> in de AKN-identificatie <sch:value-of select="$Work"/> is niet toegestaan bij besluit. Pas dit veld aan.", "ernst": "fout"},</sch:report>
         <sch:p>AKN-identificatie (work) van (evt gecons) regeling of tijdelijkregelingdeel MOET als
        derde deel act hebben</sch:p>
         <sch:report id="STOP1012"
                     test="$is_regeling and not(matches($Work_documenttype, '^act$'))"
                     role="fout">
	    {"code": "STOP1012", "Work-ID": "<sch:value-of select="$Work"/>", "substring": "<sch:value-of select="$Work_documenttype"/>", "melding": "Derde veld <sch:value-of select="$Work_documenttype"/> in de AKN-identificatie <sch:value-of select="$Work"/> is niet toegestaan bij regeling. Pas dit veld aan.", "ernst": "fout"},</sch:report>
         <sch:p>JOIN-identificatie (expressie) MOET als eerste deel na de '@' een jaartal of een
        geldige datum hebben groter/gelijk aan jaartal in werk</sch:p>
         <sch:report id="STOP1008"
                     test="$is_join and not($Expression_datum_expr &gt;= $Expression_datum_work)"
                     role="fout"> 
		  {"code": "STOP1008", "Work-ID": "<sch:value-of select="$Work"/>", "Expression-ID": "<sch:value-of select="$Expression"/>", "melding": "JOIN-identificatie (<sch:value-of select="$Expression"/>) MOET als eerste deel na de '@' een jaartal of een geldige datum hebben groter/gelijk aan jaartal in werk (<sch:value-of select="$Work"/>). Pas dit aan.", "ernst": "fout"},</sch:report>
         <!-- STOP1017 vervallen -->
         <sch:p>AKN-identificatie van een kennisgeving of mededeling MOET als derde deel doc
        hebben</sch:p>
         <sch:report id="STOP1037"
                     test="($is_kennisgeving or $is_mededeling) and not(matches($Work_documenttype, '^doc$'))"
                     role="fout">
	    {"code": "STOP1037", "Work-ID": "<sch:value-of select="$Work"/>", "substring": "<sch:value-of select="$Work_documenttype"/>", "melding": "Derde veld <sch:value-of select="$Work_documenttype"/> in de AKN-identificatie <sch:value-of select="$Work"/> is niet toegestaan voor een kennisgeving of mededeling. Pas dit veld aan.", "ernst": "fout"},</sch:report>
         <sch:p>AKN-identificatie van een rectificatie MOET als derde deel doc hebben</sch:p>
         <sch:report id="STOP1044"
                     test="$is_rectificatie and not(matches($Work_documenttype, '^doc$'))"
                     role="fout">
	    {"code": "STOP1044", "Work-ID": "<sch:value-of select="$Work"/>", "substring": "<sch:value-of select="$Work_documenttype"/>", "melding": "Derde deel <sch:value-of select="$Work_documenttype"/> in de AKN-identificatie <sch:value-of select="$Work"/> is niet toegestaan voor een rectificatie. Pas dit deel aan.", "ernst": "fout"},</sch:report>
         <sch:p>Als FRBRWork begint met '/akn/nl/bill/' dan moet het soortwork '/join/id/stop/work_003'
        (generiek besluit) zijn.</sch:p>
         <sch:report id="STOP2002"
                     test="matches($Work_documenttype, '^bill$') and not($is_besluit)"
                     role="fout">
	    {"code": "STOP2002", "Work-ID": "<sch:value-of select="$Work"/>", "soortWork": "<sch:value-of select="$soortWork"/>", "melding": "FRBRWork '<sch:value-of select="$Work"/>' begint met '/akn/nl/bill/' maar soortwork'<sch:value-of select="$soortWork"/>' is niet gelijk aan '/join/id/stop/work_003'(besluit).", "ernst": "fout"},</sch:report>
         <sch:p>Als FRBRWork begint met "/akn/nl/act/" dan moet het soortwork "/join/id/stop/work_019"
        (regeling), of "/join/id/stop/work_006"  (geconsolideerde regeling), of 
        "/join/id/stop/work_021" (tijdelijk regelingdeel), of  "/join/id/stop/work_022"
        (consolidatie van tijdelijk regelingdeel) zijn.</sch:p>
         <sch:report id="STOP2003"
                     test="matches($Work_documenttype, '^act$') and not($is_regeling)"
                     role="fout">
	    {"code": "STOP2003", "Work-ID": "<sch:value-of select="$Work"/>", "soortWork": "<sch:value-of select="$soortWork"/>", "melding": "FRBRWork '<sch:value-of select="$Work"/>' begint met '/akn/nl/act/' maar soortwork <sch:value-of select="$soortWork"/>' is niet gelijk aan '/join/id/stop/work_019'(Regeling), '/join/id/stop/work_006'(Geconsolideerde regeling), '/join/id/stop/work_021'(Tijdelijk regelingdeel) of '/join/id/stop/work_022'(Consolidatie van tijdelijk regelingdeel).", "ernst": "fout"},</sch:report>
         <sch:p>als FRBRWork begint met "/akn/nl/doc/" dan moet soortwork "/join/id/stop/work_018"
        (rectificatie), "/join/id/stop/work_023" (kennisgeving) of "/join/id/stop/work_025"
        (mededeling) zijn.</sch:p>
         <sch:report id="STOP2052"
                     test="matches($Work_documenttype, '^doc$') and not($is_rectificatie or $is_kennisgeving or $is_mededeling)"
                     role="fout">
	    {"code": "STOP2052", "Work-ID": "<sch:value-of select="$Work"/>", "soortWork": "<sch:value-of select="$soortWork"/>", "melding": "FRBRWork '<sch:value-of select="$Work"/>' begint met '/akn/nl/doc/' maar soortwork <sch:value-of select="$soortWork"/>' is niet gelijk aan '/join/id/stop/work_018'(rectificatie), '/join/id/stop/work_023'(kennisgeving) of '/join/id/stop/work_025'(mededeling).", "ernst": "fout"},</sch:report>
         <sch:p>als FRBRWork begint met "/join/id" dan moet soortwork "/join/id/stop/work_010"
        (informatieobject) of "/join/id/stop/work_005" (geconsolideerd informatieobject)
        zijn.</sch:p>
         <sch:report id="STOP2024"
                     test="(matches($Work_objecttype, '^id$')) and not($is_informatieobject or $is_cons_informatieobject)"
                     role="fout">
	    {"code": "STOP2024", "Work-ID": "<sch:value-of select="$Work"/>", "soortWork": "<sch:value-of select="$soortWork"/>", "melding": "FRBRWork '<sch:value-of select="$Work"/>' begint met '/join/id' maar soortwork <sch:value-of select="$soortWork"/>' is niet gelijk aan '/join/id/stop/work_010'(informatieobject) of '/join/id/stop/work_005'(geconsolideerd informatieobject).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_058">
      <sch:rule context="data:ExpressionIdentificatie[data:soortWork = '/join/id/stop/work_021']">
         <sch:p>De identificatie van een tijdelijk regelingdeel (data:soortWork =
        '/join/id/stop/work_021') MOET aangeven waarvan het een tijdelijk deel is (heeft
        data:isTijdelijkDeelVan).</sch:p>
         <sch:assert id="STOP2058" test="child::data:isTijdelijkDeelVan" role="fout">
	    {"code": "STOP2058", "Work-ID": "<sch:value-of select="data:FRBRWork"/>", "melding": "De ExpressionIdentificatie('<sch:value-of select="data:FRBRWork"/>') is van een tijdelijk regelingdeel (data:soortWork = '/join/id/stop/work_021') maar deze geeft niet aan van welke regeling het een tijdelijk deel is. Voeg data:isTijdelijkDeelVan toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_data_006">
      <sch:title>Tijdelijk regelingdeel</sch:title>
      <sch:rule context="data:isTijdelijkDeelVan">
         <sch:let name="soortWorkTijdelijkdeel"
                  value="parent::data:ExpressionIdentificatie/data:soortWork/string()"/>
         <sch:let name="workTijdelijkdeel"
                  value="parent::data:ExpressionIdentificatie/data:FRBRWork/string()"/>
         <sch:let name="workTijdelijkdeel_reeks"
                  value="tokenize($workTijdelijkdeel, '/')"/>
         <sch:let name="workTijdelijkDeel_documenttype"
                  value="$workTijdelijkdeel_reeks[4]"/>
         <sch:let name="soortWorkVanRegeling"
                  value="data:WorkIdentificatie/data:soortWork/string()"/>
         <sch:let name="workVanRegeling"
                  value="data:WorkIdentificatie/data:FRBRWork/string()"/>
         <sch:let name="workVanRegeling_reeks" value="tokenize($workVanRegeling, '/')"/>
         <sch:let name="workVanRegeling_documenttype" value="$workVanRegeling_reeks[4]"/>
         <sch:let name="is_tijdelijkregelingdeel"
                  value="$soortWorkTijdelijkdeel = '/join/id/stop/work_021'"/>
         <sch:let name="is_regeling"
                  value="$soortWorkVanRegeling = '/join/id/stop/work_019'"/>
         <sch:p>De identificatie van een tijdelijk regelingdeel (data:ExpressionIdentificatie bevat
        data:isTijdelijkDeelVan) MOET als soortWork '/join/id/stop/work_021' (tijdelijk
        regelingdeel) hebben.</sch:p>
         <sch:assert id="STOP2004" test="$is_tijdelijkregelingdeel" role="fout">
        {"code": "STOP2004", "soortWork": "<sch:value-of select="$soortWorkTijdelijkdeel"/>", "melding": "De ExpressionIdentificatie bevat data:isTijdelijkDeelVan, maar data:soortWork('<sch:value-of select="$soortWorkTijdelijkdeel"/>') is niet gelijk aan '/join/id/stop/work_021'(tijdelijk regelingdeel). Pas soortWork aan.", "ernst": "fout"},</sch:assert>
         <sch:p>De identificatie van een tijdelijk regelingdeel (ExpressionIdentificatie bevat
        data:isTijdelijkDeelVan) MOET tijdelijk deel zijn van een regeling met soortWork
        '/join/id/stop/work_019' (regeling).</sch:p>
         <sch:assert id="STOP2057" test="$is_regeling" role="fout">
        {"code": "STOP2057", "soortWork": "<sch:value-of select="$soortWorkVanRegeling"/>", "melding": "De ExpressionIdentificatie bevat data:isTijdelijkDeelVan, maar het soortWork('<sch:value-of select="$soortWorkVanRegeling"/>') van de regeling waar deze regeling een tijdelijk deel van is, is niet gelijk aan '/join/id/stop/work_019' (regeling). Pas soortWork aan.", "ernst": "fout"},</sch:assert>
         <sch:p>ALS het soortwork van het Work waar een tijdelijk regelingdeel toe behoort
        '/join/id/stop/work_019' (regeling) is, DAN MOET het derde deel van het FRBRWork '/act/'
        zijn.</sch:p>
         <sch:assert id="STOP2063"
                     test="$workVanRegeling_documenttype = 'act'"
                     role="fout">
      {"code": "STOP2063", "Work-id": "<sch:value-of select="$workVanRegeling"/>", "melding": "De ExpressionIdentificatie bevat een isTijdelijkdeelVan:WorkIdentificatie:soortWork met '/join/id/stop/work_019' (regeling), maar het derde deel van isTijdelijkdeelVan:WorkIdentificatie:FRBRWork('<sch:value-of select="$workVanRegeling"/>') is niet gelijk aan '/act/'. Pas FRBRWork aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
</sch:schema>
