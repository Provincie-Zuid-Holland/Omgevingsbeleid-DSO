<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="tekst" uri="https://standaarden.overheid.nl/stop/imop/tekst/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validatie voor tekstmutaties</sch:p>
   <!--
    Initiële regelingen
  -->
   <sch:pattern id="sch_tekst_024">
      <sch:title>Regelingen - initieel met componentnaam</sch:title>
      <sch:rule context="tekst:BesluitKlassiek/tekst:RegelingKlassiek | tekst:WijzigBijlage/tekst:RegelingCompact | tekst:WijzigBijlage/tekst:RegelingVrijetekst | tekst:WijzigBijlage/tekst:RegelingTijdelijkdeel">
         <sch:let name="regeling">
            <xsl:choose>
               <xsl:when test="child::tekst:RegelingOpschrift">
                  <xsl:value-of select="string-join(child::tekst:RegelingOpschrift/*/normalize-space(), '')"/>
               </xsl:when>
               <xsl:otherwise>
                  <xsl:value-of select="string-join(tekst:*/tekst:RegelingOpschrift/*/normalize-space(), '')"/>
               </xsl:otherwise>
            </xsl:choose>
         </sch:let>
         <sch:assert id="STOP0024" test="@componentnaam" role="fout"> {"code": "STOP0024", "regeling": "<sch:value-of select="$regeling"/>", "melding": "De initiële regeling \"<sch:value-of select="$regeling"/>\" heeft geen attribuut @componentnaam, dit attribuut is voor een initiële regeling verplicht. Voeg het attribuut toe met een unieke naamgeving.", "ernst": "fout"},</sch:assert>
         <sch:assert id="STOP0025" test="@wordt" role="fout"> {"code": "STOP0025", "regeling": "<sch:value-of select="$regeling"/>", "melding": "De initiële regeling \"<sch:value-of select="$regeling"/>\" heeft geen attribuut @wordt, dit attribuut is voor een initiële regeling verplicht. Voeg het attribuut toe met als waarde de juiste AKN versie-identifier", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!--
    Unieke componentnamen
  -->
   <sch:pattern id="sch_tekst_031">
      <sch:title>Identificatie - componentnaam uniek</sch:title>
      <sch:rule context="tekst:*[@componentnaam]">
         <sch:let name="mijnComponent" value="@componentnaam"/>
         <sch:assert id="STOP0026"
                     test="count(//tekst:*[@componentnaam = $mijnComponent]) = 1"
                     role="fout"> {"code": "STOP0026", "component": "<sch:value-of select="$mijnComponent"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "De componentnaam \"<sch:value-of select="$mijnComponent"/> binnen <sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/> is niet uniek. Pas de componentnaam aan om deze uniek te maken", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_073">
    <!-- geen wijziglid in compact -->
      <sch:title>BesluitCompact WijzigArtikel zonder WijzigLid</sch:title>
      <sch:rule context="tekst:BesluitCompact//tekst:WijzigArtikel[not(ancestor::tekst:RegelingCompact)]">
         <sch:p>Een WijzigArtikel in een BesluitCompact MAG GEEN Wijziglid bevatten</sch:p>
         <sch:report id="STOP0073" test="child::tekst:WijzigLid" role="fout">
        {"code": "STOP0073", "id": "<sch:value-of select="@eId"/>", "melding": "Het WijzigArtikel <sch:value-of select="@eId"/> heeft een WijzigLid, dit is niet toegestaan binnen een BesluitCompact. Verwijder het WijzigL:id of zet de tekst om naar een element wat.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <!--
    Unieke wordt
  -->
   <sch:pattern id="sch_tekst_032">
      <sch:title>Identificatie - wordt uniek</sch:title>
      <sch:rule context="tekst:*[@wordt]">
         <sch:let name="mijnWordt" value="@wordt"/>
         <sch:assert id="STOP0074"
                     test="count(//tekst:*[@wordt= $mijnWordt]) = 1"
                     role="fout"> 
        {"code": "STOP0074", "wordt": "<sch:value-of select="$mijnWordt"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het attribuut @wordt '<sch:value-of select="$mijnWordt"/>' binnen <sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/> is niet uniek. Pas het attribuut aan om deze uniek te maken (bij een initiele regeling) of (bij mutaties) voeg mutaties samen in één tekst:RegelingMutatie .", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!--
    Unieke ID's binnen componenten
  -->
   <!-- 2023-10-11 STOP0027/28 aangepast: keys toegevoegd, uitzondering voor verwijderde wId weggehaald (STOP0028).
    			Een verwijderde eId(STOP0027) kan opnieuw worden toegekend (bij hernummering). De verwijderde eId moet dan een 
    			_instX toevoeging moeten krijgen, zodat eId ook uniek is. 
    			Een verwijderde wId mag nooit opnieuw worden gebruikt, bij herintroductie van een verwijderde wId moet
    			tenminste het versienummer wijzigen zodat de wId uniek is. AD
			-->
   <xsl:key match="tekst:*[@eId][ancestor::tekst:*[@componentnaam]][not(ancestor::tekst:WijzigInstructies)]"
            name="alleEIDs"
            use="@eId"/>
   <xsl:key match="tekst:*[@wId][ancestor::tekst:*[@componentnaam]][not(ancestor::tekst:WijzigInstructies)]"
            name="alleWIDs"
            use="@wId"/>
   <sch:pattern id="sch_tekst_012_1">
      <sch:title>Identificatie - eId, wId binnen een AKN-component</sch:title>
      <sch:rule context="tekst:*[@componentnaam]">
         <sch:let name="mijnComponent" value="@componentnaam"/>
         <sch:let name="eId-fout">
            <xsl:for-each-group select=".//tekst:*[@eId]" group-by="@eId">
               <xsl:if test="count(key('alleEIDs',@eId)[ancestor::tekst:*[@componentnaam][1][@componentnaam=$mijnComponent]])&gt;1">
                  <xsl:value-of select="./@eId"/>
                  <xsl:text>; </xsl:text>
               </xsl:if>
            </xsl:for-each-group>
         </sch:let>
         <sch:let name="eId-fout-netjes" value="replace($eId-fout,'; $','')"/>
         <sch:let name="wId-fout">
            <xsl:for-each-group select=".//tekst:*[@wId]" group-by="@wId">
               <xsl:if test="count(key('alleWIDs',@wId)[ancestor::tekst:*[@componentnaam][1][@componentnaam=$mijnComponent]])&gt;1">
                  <xsl:value-of select="./@wId"/>
                  <xsl:text>; </xsl:text>
               </xsl:if>
            </xsl:for-each-group>
         </sch:let>
         <sch:let name="wId-fout-netjes" value="replace($wId-fout,'; $','')"/>
         <sch:assert id="STOP0027" test="$eId-fout-netjes = ''" role="fout"> 
						{"code": "STOP0027", "eId": "<sch:value-of select="$eId-fout-netjes"/>", "component": "<sch:value-of select="$mijnComponent"/>", "melding": "De eId '<sch:value-of select="$eId-fout-netjes"/>' binnen component <sch:value-of select="$mijnComponent"/> moet uniek zijn. Controleer de opbouw van de eId en corrigeer deze", "ernst": "fout"},
					</sch:assert>
         <sch:assert id="STOP0028" test="$wId-fout-netjes = ''" role="fout">
						{"code": "STOP0028", "wId": "<sch:value-of select="$wId-fout-netjes"/>", "component": "<sch:value-of select="$mijnComponent"/>", "melding": "De wId '<sch:value-of select="$wId-fout-netjes"/>' binnen component <sch:value-of select="$mijnComponent"/> moet uniek zijn. Controleer de opbouw van de wId en corrigeer deze", "ernst": "fout"},
					</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_018">
      <sch:title>RegelingMutatie - WijzigInstructies in een WijzigArtikel</sch:title>
      <sch:rule context="tekst:WijzigArtikel//tekst:WijzigInstructies">
         <sch:assert id="STOP0039" test="ancestor::tekst:RegelingKlassiek" role="fout"> {"code": "STOP0039", "naam": "<sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het element WijzigInstructies binnen element <sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/> met eId \"<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>\" is niet toegestaan. Verwijder de WijzigInstructies, of verplaats deze naar een RegelingMutatie binnen een WijzigBijlage.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_048">
      <sch:title>RegelingMutatie - OpmerkingVersie in een WijzigArtikel</sch:title>
      <sch:rule context="tekst:WijzigArtikel//tekst:OpmerkingVersie">
         <sch:assert id="STOP0051"
                     test="ancestor::tekst:RegelingKlassiek or ancestor::tekst:Rectificatie"
                     role="fout"> {"code": "STOP0051", "naam": "<sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het element OpmerkingVersie binnen element <sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/> met eId \"<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>\" is alleen toegestaan in een RegelingKlassiek of Rectificatie daarvan. Verwijder de OpmerkingVersie.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_019">
      <sch:title>RegelingMutatie - in een WijzigArtikel alleen in RegelingKlassiek</sch:title>
      <sch:rule context="tekst:WijzigArtikel//tekst:RegelingMutatie">
         <sch:assert id="STOP0040"
                     test="ancestor::tekst:Lichaam/parent::tekst:RegelingKlassiek"
                     role="fout"> {"code": "STOP0040", "naam": "<sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het element RegelingMutatie binnen element <sch:value-of select="local-name(ancestor::tekst:*[@eId][1])"/> met eId \"<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>\" is niet toegestaan. Neem de RegelingMutatie op in een WijzigBijlage.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0045">
      <sch:title>@Wijzigactie voor Inhoud</sch:title>
      <sch:rule context="tekst:Vervang//tekst:Inhoud[@wijzigactie]">
         <sch:p>tekst:Inhoud mag uitsluitend een @wijzigactie hebben gecombineerd met tekst:Vervallen,
         tekst:Gereserveerd tekst:NogNietInWerking of tekst:Lid (voor Artikel)</sch:p>
         <sch:assert id="STOP0063"
                     test="parent::tekst:*/tekst:Gereserveerd | parent::tekst:*/tekst:Vervallen | parent::tekst:*/tekst:NogNietInWerking | parent::tekst:*/tekst:Lid"
                     role="fout">{"code": "STOP0063", "naam": "<sch:value-of select="local-name(ancestor::tekst:Vervang[@wat][1])"/>", "wat": "<sch:value-of select="ancestor::tekst:Vervang[@wat][1]/@wat"/>", "melding": "Het element Inhoud van <sch:value-of select="local-name(ancestor::tekst:Vervang[@wat][1])"/> met attribuut @wat \"<sch:value-of select="ancestor::tekst:Vervang[@wat][1]/@wat"/>\" heeft ten onrechte een attribuut @wijzigactie. Dit is alleen toegestaan indien gecombineerd met Gereserveerd, Vervallen, NogNietInWerking of Lid (binnen Artikel). Verwijder het attribuut @wijzigactie.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_066">
      <sch:rule context="*[@wordt][@was]">
         <sch:let name="wasWork" value="substring-before(@was/./string(), '@')"/>
         <sch:let name="wordtWork" value="substring-before(@wordt/./string(), '@')"/>
         <sch:p>@was en @wordt moeten hetzelfde work hebben</sch:p>
         <sch:assert id="STOP0066" test="$wasWork = $wordtWork" role="fout">
      {"code": "STOP0066", "wasID": "<sch:value-of select="$wasWork"/>", "wordtID": "<sch:value-of select="$wordtWork"/>", "melding": "De identificatie van de @was <sch:value-of select="$wasWork"/> en @wordt <sch:value-of select="$wordtWork"/> hebben niet dezelfde work-identificatie. Corrigeer de AKN-expression identificatie.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_068">
      <sch:title>Noot unieke ids</sch:title>
      <sch:rule context="tekst:*[@componentnaam]">
         <sch:let name="component" value="@componentnaam"/>
         <sch:let name="nootIndex">
            <xsl:for-each select="//tekst:Noot[ancestor::tekst:*[@componentnaam][1][@componentnaam = $component]][not(ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'])][not(ancestor::tekst:Verwijder)]">
               <xsl:sort select="@id"/>
               <n>
                  <xsl:value-of select="@id"/>
               </n>
            </xsl:for-each>
         </sch:let>
         <sch:let name="nootId-fout">
            <xsl:for-each select="$nootIndex/n[preceding-sibling::n = .]">
               <xsl:value-of select="self::n/."/>
               <xsl:if test="not(position() = last())">
                  <xsl:text>; </xsl:text>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP0067" test="$nootId-fout = ''" role="fout">
      {"code": "STOP0067", "id": "<sch:value-of select="$nootId-fout"/>", "component": "<sch:value-of select="$component"/>", "melding": "De id voor tekst:Noot '<sch:value-of select="$nootId-fout"/>' binnen component '<sch:value-of select="$component"/>' moet uniek zijn. Controleer de id en corrigeer zodat de identificatie uniek is binnen de component.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <!-- STOP1500 vervallen -->
   <sch:pattern id="sch_tekst_0077">
      <sch:title>Wat moet overeenkomen met wId</sch:title>
      <sch:rule context="tekst:Vervang | tekst:Verwijder">
         <sch:assert id="STOP0077"
                     test="@wat = child::tekst:*[@wId][1]/@wId"
                     role="fout">
  {"code": "STOP0077", "watID": "<sch:value-of select="@wat"/>", "wId": "<sch:value-of select="child::tekst:*[@wId][1]/@wId"/>", "element": "<sch:value-of select="local-name(.)"/>", "melding": "De identificatie in attribuut @wat \"<sch:value-of select="@wat"/>\" in het in element <sch:value-of select="local-name(.)"/> is niet gelijk aan de wId \"<sch:value-of select="child::tekst:*[@wId][1]/@wId"/>\" van het element dat verwijderd of vervangen wordt", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0080">
      <sch:rule context="tekst:WijzigArtikel[ancestor::tekst:RegelingMutatie]">
         <sch:assert id="STOP0080" test="ancestor::tekst:Rectificatie" role="fout">
     {"code": "STOP0080", "eId": "<sch:value-of select="@eId"/>", "melding": "Het element WijzigArtikel met <sch:value-of select="@eId"/> mag alleen worden gebruikt in een RegelingMutatie binnen een Rectificatie. Verwijder het WijzigArtikel.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0086">
      <sch:title>Renvooi verplicht in Vervang/VervangKop</sch:title>
      <sch:rule context="tekst:Vervang|tekst:VervangKop">
         <sch:assert id="STOP0086"
                     test="exists(@context) or @revisie/string() = '1' or .//tekst:NieuweTekst or .//tekst:VerwijderdeTekst or .//tekst:*[@wijzigactie]"
                     role="fout">
        {"code": "STOP0086", "element": "<sch:value-of select="local-name(.)"/>", "wat": "<sch:value-of select="@wat/string()"/>", "parent": "<sch:value-of select="local-name(..)"/>", "component": "<sch:value-of select="../@componentnaam/string()"/>", "melding": "Het element <sch:value-of select="local-name(.)"/>(@wat='<sch:value-of select="@wat/string()"/>') binnen <sch:value-of select="local-name(..)"/>(@componentnaam='<sch:value-of select="../@componentnaam/string()"/>') bevat geen renvooimarkering. Dit is niet toegestaan. Voeg tekst:NieuweTekst, tekst:VerwijderdeTekst of het attribuut wijzigactie toe op de plaats van de tekstwijziging binnen <sch:value-of select="local-name(.)"/>.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0118">
      <sch:title>geen renvooi in renvooi</sch:title>
      <sch:rule context="tekst:NieuweTekst | tekst:VerwijderdeTekst">
         <sch:report id="STOP0118"
                     test="ancestor::tekst:NieuweTekst or ancestor::tekst:VerwijderdeTekst"
                     role="fout"> {"code": "STOP0118", "element": "<sch:value-of select="node-name(.)"/>", "parent": "<sch:value-of select="node-name((ancestor::tekst:NieuweTekst[1] | ancestor::tekst:VerwijderdeTekst[1])[1])"/>", "fragment": "<sch:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>", "fragment-eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het element <sch:value-of select="node-name(.)"/> staat binnen <sch:value-of select="node-name((ancestor::tekst:NieuweTekst[1] | ancestor::tekst:VerwijderdeTekst[1])[1])"/> in <sch:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>(<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>). Dit is niet toegestaan. Verwijder het renvooi-element uit de wijziging.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0119">
      <sch:title>@context en @positie altijd samen</sch:title>
      <sch:rule context="tekst:Vervang">
         <sch:let name="ontbrekend">
            <xsl:if test="(empty(@positie) and @context) or (@positie and empty(@context))">
               <xsl:if test="empty(@positie)">positie</xsl:if>
               <xsl:if test="empty(@context)">context</xsl:if>
            </xsl:if>
         </sch:let>
         <sch:let name="element">
            <xsl:for-each select="child::tekst:*">
               <xsl:choose>
                  <xsl:when test="matches(local-name(), 'Wat')"/>
                  <xsl:when test="matches(local-name(), 'Nummer')"/>
                  <xsl:otherwise>
                     <xsl:value-of select="local-name()"/>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:for-each>
         </sch:let>
         <sch:report id="STOP0119"
                     test="(not(@context) and @positie) or (not(@positie) and @context)"
                     role="fout"> {"code": "STOP0119", "element": "<sch:value-of select="$element"/>", "ontbrekendattribuut": "<sch:value-of select="$ontbrekend"/>", "attribuut": "<sch:value-of select="concat(node-name(@context), node-name(@positie))"/>", "wId": "<sch:value-of select="child::tekst:*/@wId"/>", "melding": "Het attribuut <sch:value-of select="concat(node-name(@context), node-name(@positie))"/> komt voor op tekst:Vervang van <sch:value-of select="$element"/>(<sch:value-of select="child::tekst:*/@wId"/>) terwijl attribuut <sch:value-of select="$ontbrekend"/> ontbreekt. Dit is niet toegestaan. Voeg attribuut <sch:value-of select="$ontbrekend"/> toe.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0122">
      <sch:title>Redactioneel niet in besluitcompact</sch:title>
      <sch:rule context="tekst:BesluitCompact/tekst:Lichaam//tekst:Redactioneel">
         <sch:report id="STOP0122" test="." role="fout"> {"code": "STOP0122", "element": "<sch:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>", "eId": "<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>", "melding": "Het element Redactioneel binnen <sch:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>(<sch:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>) staat in het besluitdeel van het Besluit. Dit is niet toegestaan. Verwijder het element Redactioneel.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0123">
      <sch:title>@context/@positie uniek</sch:title>
      <sch:rule context="tekst:*[@context][@positie]">
         <sch:let name="mijnContext" value="@context"/>
         <sch:let name="mijnPositie" value="@positie"/>
         <sch:assert id="STOP0123"
                     test="count(../tekst:*[@context = $mijnContext][@positie = $mijnPositie]) = 1"
                     role="fout"> 
        {"code": "STOP0123", "element": "<sch:value-of select="node-name(.)"/>", "context": "<sch:value-of select="$mijnContext"/>", "positie": "<sch:value-of select="$mijnPositie"/>", "melding": "De combinatie van attributen @context=\"<sch:value-of select="$mijnContext"/>\" en @positie=\"<sch:value-of select="$mijnPositie"/>\" op element <sch:value-of select="node-name(.)"/> is niet uniek. Hierdoor kent de RegelingMutatie geen eenduidige interpretatie. Maak elke combinatie van @positie en @context binnen RegelingMutatie uniek.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0124">
      <sch:title>verwijderd element niet gebruiken als @context</sch:title>
      <sch:rule context="tekst:*[@context]">
         <sch:let name="mijnwId" value="@context"/>
         <sch:report id="STOP0124"
                     test="../tekst:Verwijder[@wat = $mijnwId] or ..//tekst:*[@wId = $mijnwId][@wijzigactie='verwijder'] or ..//tekst:*[@wId = $mijnwId][ancestor::tekst:Verwijder] or ..//tekst:*[@wId = $mijnwId][ancestor::tekst:*[@wijzigactie='verwijder']]"
                     role="fout"> 
        {"code": "STOP0124", "element": "<sch:value-of select="node-name(.)"/>", "wId": "<sch:value-of select="$mijnwId"/>", "melding": "Het te verwijderen element met wId <sch:value-of select="$mijnwId"/> wordt als @context gebruikt op element <sch:value-of select="node-name(.)"/>. Dit is niet toegestaan. Gebruik de wId van een element dat niet verwijderd wordt als @context.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0126">
      <sch:title>Alleen @wijzigactie verwijderContainer op element dat zelf vervangen wordt</sch:title>
      <sch:rule context="tekst:Vervang/tekst:*[@wijzigactie] "> 
      <!-- uitzondering voor wijzigactie op Vervang/Nummer, wordt afgevangen door STOP0127 -->
         <sch:assert id="STOP0126"
                     test="matches(@wijzigactie/string(), '^verwijderContainer$') or matches(local-name(.), '^Nummer$')"
                     role="fout"> 
        {"code": "STOP0126", "mutatie-element": "<sch:value-of select="node-name(..)"/>", "wat": "<sch:value-of select="../@wat"/>", "element": "<sch:value-of select="node-name(.)"/>", "actie": "<sch:value-of select="@wijzigactie"/>", "melding": "Het element <sch:value-of select="node-name(..)"/>(wat=<sch:value-of select="../@wat"/>) vervangt element <sch:value-of select="node-name(.)"/> met wijzigactie=\"<sch:value-of select="@wijzigactie"/>\". Deze wijzigactie is hier niet toegestaan. Verwijder het attribuut wijzigactie of wijzig het in verwijderContainer.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0127">
      <sch:title>Geen @wijzigactie op Nummer binnen Vervang</sch:title>
      <sch:rule context="tekst:Nummer[@wijzigactie][parent::tekst:Vervang|parent::tekst:VervangKop]">
         <sch:report id="STOP0127" test="." role="fout"> 
        {"code": "STOP0127", "element": "<sch:value-of select="node-name(..)"/>", "actie": "<sch:value-of select="@wijzigactie"/>", "wat": "<sch:value-of select="../@wat"/>", "melding": "Het element Nummer binnen <sch:value-of select="node-name(..)"/>(@wat=\"<sch:value-of select="../@wat"/>\") heeft een attribuut wijzigactie=\"<sch:value-of select="@wijzigactie"/>\". Het attribuut wijzigactie is hier niet toegestaan. Verwijder het attribuut wijzigactie.", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_tekst_0128">
      <sch:title>Renvooi niet toegestaan in Vervang als @revisie = '1' aanwezig</sch:title>
      <sch:rule id="STOP0128" context="tekst:Vervang[@revisie = 1]">
         <sch:report test=".//tekst:NieuweTekst or .//tekst:VerwijderdeTekst or .//tekst:*[@wijzigactie] or exists(@context)"
                     role="fout">
        {"code": "STOP0128", "element": "<sch:value-of select="local-name(.)"/>", "wat": "<sch:value-of select="@wat/string()"/>", "parent": "<sch:value-of select="local-name(..)"/>", "component": "<sch:value-of select="../@componentnaam/string()"/>", "melding": "Het element <sch:value-of select="local-name(.)"/>(@wat='<sch:value-of select="@wat/string()"/>') binnen <sch:value-of select="local-name(..)"/>(@componentnaam='<sch:value-of select="../@componentnaam/string()"/>') bevat een verplaatsing en/of een renvooimarkering terwijl het een niet-juridische wijziging betreft (@revisie='1'). Dit is niet toegestaan. Verwijder het attribuut @revisie='1', maak de verplaatsing ongedaan ( verwijder @context en @positie) of verwijder de renvooi (tekst:NieuweTekst, tekst:VerwijderdeTekst, attribuut @wijzigactie binnen <sch:value-of select="local-name(.)"/>).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
</sch:schema>
