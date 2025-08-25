<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="data" uri="https://standaarden.overheid.nl/stop/imop/data/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron om procedureverloop bedrijfregels te valideren.
    Van toepassing op elk Procedureverloop evt. na verwerking van een procedureverloopmutatie</sch:p>
   <!-- verplichte aanwezigheid van meerInformatie als soortStap = 023, begin voorlopige voorziening -->
   <sch:pattern id="stop_1323">
      <sch:rule context="data:Procedurestap[data:soortStap = '/join/id/stop/procedure/stap_023']">
         <sch:assert id="STOP1323" test="data:meerInformatie" role="fout">
        {"code": "STOP1323", "soortStap": "/join/id/stop/procedure/stap_023", "datumStap": "<sch:value-of select="./data:voltooidOp"/>", "melding": "De stap /join/id/stop/procedure/stap_023 op datum (<sch:value-of select="./data:voltooidOp"/>) heeft geen data:meerInformatie verwijzing. Bij deze stap is deze verwijzing verplicht. Voeg een data:meerInformatie verwijzing toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!-- 
      Schematrons zijn zo generiek mogelijk opgezet en onafhankelijk van de waardelijst-waarde per stap. 
      
      Aanpak: 
      Alle voorkomende stappen in het procedureverloop worden gekopieerd
      en er wordt extra validatie-informatie aan de stappen toegevoegd.
      - Als een stap maar één keer voor mag komen wordt uniek = 1 gezet - STOP1302
      - Er zijn drie type stappen: algemeen, specifiek voor ontwerp(exclusief_voor_ontwerp) en specifiek  
        voor definitief besluit(exclusief_voor_definitief) - STOP1301
      - Een aantal stappen heeft een vaste volgorde. Daarbij kunnen de meeste opeenvolgende
        stappen op dezelfde datum plaatsvinden; als dat niet zo is staat bij de opvolgende 
        stap '_lateredatum'. Dat valt uiteen in drie reeksen:
        besluit: vaststelling t/m publicatie (en voor ontwerp beperking vindbaarheid) (besluit_volgorde) - STOP1303
        reactie: vaststelling en/of ondertekening plus inzage/bezwaar/beroeptermijnen. (reactie_volgorde / reactie_lateredatum) - STOP1304
        beroep: vaststelling en/of ondertekening, beroep ingesteld, einde beroepstermijn. (beroep_volgorde / beroep_lateredatum) - STOP1305
      - De andere stappen betreffen periodes (beroep-deze niet meer/schorsing-deze nog wel) en
        groepen van deze stappen kunnen repeteren(schorsing).
        Hiervan wordt aangegeven of het een start of einde betreft van: in_beroep of voorlopige voorziening (vovo).
        Ook wordt aangegeven of een stap binnen (in) een van de perioden moet vallen (op dit
        moment alleen binnen een in_beroep periode).
      - Bij de bepaling van de volgorde vindt sortering op datum plaats. Sommige stappen
        mogen dezelfde datum hebben. Om bij de sortering de stappen toch op volgorde van 
        voorkomen in de procedure te zetten wordt een absolute datum_sorteervolgorde toegekend.
        Stappen met dezelfde datum worden op volgorde van datum_sorteervolgorde gezet. De 
        absolute waarde is niet van belang, dus vanaf 0 = vaststelling/publicatie,
        100 = ontwerp, 200 = definitief.
      -->
   <sch:pattern id="procedureverloop">
      <sch:rule context="data:procedurestappen">
         <sch:let name="stappen">
            <xsl:for-each select="data:Procedurestap">
               <xsl:sort select="normalize-space(data:soortStap/./string())"/>
               <xsl:sort select="substring(data:voltooidOp/./string(),1,10)"/>
               <xsl:variable name="code" select="normalize-space(data:soortStap/./string())"/>
               <stap>
                  <code>
                     <xsl:value-of select="$code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="substring(data:voltooidOp/./string(),1,10)"/>
                  </datum>
                  <xsl:choose>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_002'"> <!-- Vaststelling -->
                        <uniek>1</uniek>
                        <besluit_volgorde>1</besluit_volgorde>
                        <reactie_volgorde>1</reactie_volgorde>
                        <beroep_volgorde>1</beroep_volgorde>
                        <datum_sorteervolgorde>001</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_003'"> <!-- Ondertekening -->
                        <uniek>1</uniek>
                        <besluit_volgorde>2</besluit_volgorde>
                        <reactie_volgorde>1</reactie_volgorde>
                        <beroep_volgorde>1</beroep_volgorde>
                        <datum_sorteervolgorde>002</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_004'"> <!-- Publicatie -->
                        <uniek>1</uniek>
                        <besluit_volgorde>3</besluit_volgorde>
                        <datum_sorteervolgorde>003</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_014'"> <!-- Begin inzagetermijn -->
                        <uniek>1</uniek>
                        <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                        <reactie_volgorde>2</reactie_volgorde>
                        <datum_sorteervolgorde>101</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_005'"> <!-- Einde inzagetermijn -->
                        <uniek>1</uniek>
                        <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                        <reactie_volgorde>3</reactie_volgorde>
                        <reactie_lateredatum>1</reactie_lateredatum>
                        <datum_sorteervolgorde>102</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_015'"> <!-- Einde bezwaartermijn -->
                        <uniek>1</uniek>
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <reactie_volgorde>2</reactie_volgorde>
                        <reactie_lateredatum>1</reactie_lateredatum>
                        <datum_sorteervolgorde>201</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_018'"> <!-- Beroep(en) ingesteld -->
                        <uniek>1</uniek>
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <beroep_volgorde>2</beroep_volgorde>
                        <in_beroep>start</in_beroep>
                        <datum_sorteervolgorde>211</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_016'"> <!-- Einde beroepstermijn -->
                        <uniek>1</uniek>
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <reactie_volgorde>3</reactie_volgorde>
                        <reactie_lateredatum>1</reactie_lateredatum>
                        <beroep_volgorde>3</beroep_volgorde>
                        <datum_sorteervolgorde>212</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_021'"> <!-- Beroep(en) definitief afgedaan -->
                        <uniek>1</uniek>
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <in_beroep>einde</in_beroep>
                        <datum_sorteervolgorde>299</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_022'"> <!-- Beperking vindbaarheid -->
                        <uniek>1</uniek>
                        <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                        <besluit_volgorde>4</besluit_volgorde>
                        <besluit_lateredatum>1</besluit_lateredatum>
                        <datum_sorteervolgorde>999</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_023'"> <!-- Uitspraak voorlopige voorziening (vovo) -->
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <in_beroep>in</in_beroep>
                        <vovo>start</vovo>
                        <datum_sorteervolgorde>221</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:when test="$code = '/join/id/stop/procedure/stap_024'"> <!-- Voorlopige voorziening opgeheven/vervallen (vovo) -->
                        <exclusief_voor_definitief>1</exclusief_voor_definitief>
                        <in_beroep>in</in_beroep>
                        <vovo>einde</vovo>
                        <datum_sorteervolgorde>222</datum_sorteervolgorde>
                     </xsl:when>
                     <xsl:otherwise/>
                  </xsl:choose>
               </stap>
            </xsl:for-each>
         </sch:let>
         <!--
      Verplichte aanwezigheid van gecombineerde stappen.
      -->
         <sch:let name="Beroep_ingesteld">
            <xsl:if test="$stappen/stap[code = '/join/id/stop/procedure/stap_018']"> <!-- Beroep(en) ingesteld -->
               <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> <!-- Ondertekening -->
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_018", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_018 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
               <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_016'])"> <!-- Einde beroepstermijn -->
                {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_018", "soortStap2": "/join/id/stop/procedure/stap_016", "melding": "De stap /join/id/stop/procedure/stap_016 moet vermeld worden als ook stap /join/id/stop/procedure/stap_018 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
            </xsl:if>
         </sch:let>
         <sch:let name="Einde_beroepstermijn">
            <xsl:if test="$stappen/stap[code = '/join/id/stop/procedure/stap_016']"> <!-- Einde beroepstermijn -->
               <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> <!-- Ondertekening -->
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_016", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_016 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
            </xsl:if>
         </sch:let>
         <sch:let name="Begin_inzagetermijn">
            <xsl:if test="$stappen/stap[code = '/join/id/stop/procedure/stap_014']"> <!-- Begin inzagetermijn -->
               <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_005'])"> <!-- Einde inzagetermijn -->
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_014", "soortStap2": "/join/id/stop/procedure/stap_005", "melding": "De stap /join/id/stop/procedure/stap_005 moet vermeld worden als ook stap /join/id/stop/procedure/stap_014 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
            </xsl:if>
         </sch:let>
         <sch:let name="Einde_bezwaar">
            <xsl:if test="$stappen/stap[code = '/join/id/stop/procedure/stap_015']"> <!-- Einde bezwaar -->
               <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> <!-- Ondertekening -->
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_015", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_015 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
            </xsl:if>
         </sch:let>
         <sch:let name="json_STOP1319"
                  value="concat($Begin_inzagetermijn,$Beroep_ingesteld,$Einde_beroepstermijn,$Einde_bezwaar)"/>
         <sch:assert id="STOP1319"
                     test="normalize-space($json_STOP1319) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1319"/>
         </sch:assert>
         <!--
      In het resterende deel van deze rule komen de codes van de stappen niet meer voor.
      -->
         <!--
      De stappen zijn gesorteerd op code, daarna op datum. Detecteer dubbele stappen
      voor de stappen die uniek moeten zijn.
      -->
         <sch:let name="json_STOP1302">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="uniek = '1' and preceding-sibling::*[1]/code = code">
            {"code": "STOP1302", "soortStap": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> komt meermalen voor, als voltooid op <xsl:value-of select="datum"/> en op <xsl:value-of select="preceding-sibling::*[1]/datum"/>.", "ernst": "fout"},</xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1302"
                     test="normalize-space($json_STOP1302/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1302/./string()"/>
         </sch:assert>
         <!--
      Sorteer de stappen op datum en daarna op datum_sorteervolgorde. Ontdubbel ze, 
      zodat de testen op correctheid en volledigheid van de procedure plaats kunnen vinden.
      -->
         <sch:let name="stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:sort select="datum"/>
               <xsl:sort select="number(datum_sorteervolgorde)"/>
               <xsl:choose>
                  <xsl:when test="uniek = '1'">
                     <xsl:if test="not(preceding-sibling::*[1]/code) or preceding-sibling::*[1]/code != code">
                        <xsl:copy-of select="."/>
                     </xsl:if>
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:copy-of select="."/>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <!--
      Kijk of er stappen voorkomen die exclusief tot de ene of de andere procedure behoren
      -->
         <sch:let name="STOP1300_exclusief_voor_ontwerp">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="exclusief_voor_ontwerp = '1'">
                  <xsl:value-of select="code"/>
                  <xsl:text> (voltooid op </xsl:text>
                  <xsl:value-of select="datum"/>
                  <xsl:text>) </xsl:text>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:let name="STOP1300_exclusief_voor_definitief">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="exclusief_voor_definitief = '1'">
                  <xsl:value-of select="code"/>
                  <xsl:text> (voltooid op </xsl:text>
                  <xsl:value-of select="datum"/>
                  <xsl:text>) </xsl:text>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1300"
                     test="not ($STOP1300_exclusief_voor_definitief != '' and $STOP1300_exclusief_voor_ontwerp != '')"
                     role="fout">
        {"code": "STOP1300", "soortStap1": "<sch:value-of select="normalize-space($STOP1300_exclusief_voor_definitief)"/>", "soortStap2": "<sch:value-of select="normalize-space($STOP1300_exclusief_voor_ontwerp)"/>", "melding": "De stappen <sch:value-of select="normalize-space($STOP1300_exclusief_voor_definitief)"/> komen niet voor in dezelfde besluitvormingsprocedure als de stappen <sch:value-of select="normalize-space($STOP1300_exclusief_voor_ontwerp)"/>.", "ernst": "fout"},</sch:assert>
         <!-- 
      Onderzoek of aan de absolute volgorde van de stappen voldaan wordt 
      voor de 3 reeksen: besluit, reactie en beroep
      De schematron code is steeds hetzelfde, de naam van het attribuut
      is steeds anders.
      -->
         <!--
      Begin met besluit_volgorde
      -->
         <!--
      Selecteer de stappen waarvoor de besluit_volgorde gezet is
      de stappen staan al op datum volgorde 
      -->
         <sch:let name="STOP1303_stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="besluit_volgorde">
                  <stap>
                     <code>
                        <xsl:value-of select="code"/>
                     </code>
                     <datum>
                        <xsl:value-of select="datum"/>
                     </datum>
                     <volgorde>
                        <xsl:value-of select="besluit_volgorde"/>
                     </volgorde>
                     <lateredatum>
                        <xsl:value-of select="besluit_lateredatum"/>
                     </lateredatum>
                  </stap>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <!--
      Controleer dat de besluit_volgorde oplopend is
      -->
         <sch:let name="json_STOP1303">
            <xsl:for-each select="$STOP1303_stappen/stap">
               <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1303", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus ná de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1303"
                     test="normalize-space($json_STOP1303/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1303/./string()"/>
         </sch:assert>
         <!--
      reactie_volgorde
      -->
         <sch:let name="STOP1304_stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="reactie_volgorde">
                  <stap>
                     <code>
                        <xsl:value-of select="code"/>
                     </code>
                     <datum>
                        <xsl:value-of select="datum"/>
                     </datum>
                     <volgorde>
                        <xsl:value-of select="reactie_volgorde"/>
                     </volgorde>
                     <lateredatum>
                        <xsl:value-of select="reactie_lateredatum"/>
                     </lateredatum>
                  </stap>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:let name="json_STOP1304">
            <xsl:for-each select="$STOP1304_stappen/stap">
               <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1304", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus na de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1304"
                     test="normalize-space($json_STOP1304/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1304/./string()"/>
         </sch:assert>
         <!--
      beroep_volgorde
      -->
         <sch:let name="STOP1305_stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="beroep_volgorde">
                  <stap>
                     <code>
                        <xsl:value-of select="code"/>
                     </code>
                     <datum>
                        <xsl:value-of select="datum"/>
                     </datum>
                     <volgorde>
                        <xsl:value-of select="beroep_volgorde"/>
                     </volgorde>
                     <lateredatum>
                        <xsl:value-of select="beroep_lateredatum"/>
                     </lateredatum>
                  </stap>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:let name="json_STOP1305">
            <xsl:for-each select="$STOP1305_stappen/stap">
               <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1305", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus na de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1305"
                     test="normalize-space($json_STOP1305/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1305/./string()"/>
         </sch:assert>
         <!-- 
      Onderzoek of de stappen die begin/einde van een periode aangeven of 
      die in een periode moeten vallen, in de juiste volgorde staan.
      -->
         <!--
      in_beroep: begin / einde van de periode, of binnen een periode vallen
      Als de start van een periode ontbreekt wordt dat alleen voor het eerste
      element in de periode gerapporteerd.
      -->
         <sch:let name="STOP1310_tm_STOP1312_stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="in_beroep">
                  <stap>
                     <code>
                        <xsl:value-of select="code"/>
                     </code>
                     <datum>
                        <xsl:value-of select="datum"/>
                     </datum>
                     <fase>
                        <xsl:value-of select="in_beroep"/>
                     </fase>
                  </stap>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <!-- STOP1310 verwijderd -->
         <!-- STOP1311 Stappen die samenhangen met een voorlopige voorziening bij een besluit door een rechter 
         MOETEN in het procedureverloop na de start van de beroepsperiode opgenomen zijn. -->
         <sch:let name="json_STOP1311">
            <xsl:for-each select="$STOP1310_tm_STOP1312_stappen/stap">
               <xsl:choose>
                  <xsl:when test="fase = 'in' and (not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1311", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) ligt niet na een 'Start beroepsprocedure'.", "ernst": "fout"},</xsl:when>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1311"
                     test="normalize-space($json_STOP1311/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1311/./string()"/>
         </sch:assert>
         <sch:let name="json_STOP1312">
            <xsl:for-each select="$STOP1310_tm_STOP1312_stappen/stap">
               <xsl:choose>
                  <xsl:when test="fase = 'einde' and (preceding-sibling::*[1]/fase = 'einde' or not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1312", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het einde van een beroepsperiode, maar er is geen eerdere stap die het begin van de beroepsperiode aangeeft.", "ernst": "fout"},</xsl:when>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1312"
                     test="normalize-space($json_STOP1312/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1312/./string()"/>
         </sch:assert>
         <!--
      voorlopige voorziening (vovo): begin / einde van de periode
      (er is geen "in", dus deze test ontbreekt, verder is de code een vrijwel exacte kopie van de in_beroep code.)
      -->
         <sch:let name="STOP1313_tm_STOP1315_stappen">
            <xsl:for-each select="$stappen/stap">
               <xsl:if test="vovo">
                  <stap>
                     <code>
                        <xsl:value-of select="code"/>
                     </code>
                     <datum>
                        <xsl:value-of select="datum"/>
                     </datum>
                     <fase>
                        <xsl:value-of select="vovo"/>
                     </fase>
                  </stap>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:let name="json_STOP1313">
            <xsl:for-each select="$STOP1313_tm_STOP1315_stappen/stap">
               <xsl:choose>
                  <xsl:when test="fase = 'start' and preceding-sibling::*[1]/fase != 'einde' ">
               {"code": "STOP1313", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het begin van een voorlopige voorzieningen periode, maar de voorgaande periode is nog niet afgesloten.", "ernst": "fout"},</xsl:when>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1313"
                     test="normalize-space($json_STOP1313/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1313/./string()"/>
         </sch:assert>
         <sch:let name="json_STOP1315">
            <xsl:for-each select="$STOP1313_tm_STOP1315_stappen/stap">
               <xsl:choose>
                  <xsl:when test="fase = 'einde' and (preceding-sibling::*[1]/fase != 'start' or not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1315", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het einde van een voorlopige voorzieningen periode, maar er is geen eerdere stap die het begin van deze periode aangeeft.", "ernst": "fout"},</xsl:when>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1315"
                     test="normalize-space($json_STOP1315/./string()) = ''"
                     role="fout">
            <sch:value-of select="$json_STOP1315/./string()"/>
         </sch:assert>
      </sch:rule>
   </sch:pattern>
</sch:schema>
