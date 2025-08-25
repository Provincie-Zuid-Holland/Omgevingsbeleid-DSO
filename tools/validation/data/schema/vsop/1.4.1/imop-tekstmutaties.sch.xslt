<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
                version="2.0"><!--Implementers: please note that overriding process-prolog or process-root is 
    the preferred method for meta-stylesheets to use where possible. -->
   <xsl:param name="archiveDirParameter"/>
   <xsl:param name="archiveNameParameter"/>
   <xsl:param name="fileNameParameter"/>
   <xsl:param name="fileDirParameter"/>
   <xsl:variable name="document-uri">
      <xsl:value-of select="document-uri(/)"/>
   </xsl:variable>
   <!--PHASES-->
   <!--PROLOG-->
   <!--XSD TYPES FOR XSLT2-->
   <!--KEYS AND FUNCTIONS-->
   <xsl:key match="tekst:*[@eId][ancestor::tekst:*[@componentnaam]][not(ancestor::tekst:WijzigInstructies)]"
            name="alleEIDs"
            use="@eId"/>
   <xsl:key match="tekst:*[@wId][ancestor::tekst:*[@componentnaam]][not(ancestor::tekst:WijzigInstructies)]"
            name="alleWIDs"
            use="@wId"/>
   <!--DEFAULT RULES-->
   <!--MODE: SCHEMATRON-SELECT-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-select-full-path">
      <xsl:apply-templates select="." mode="schematron-get-full-path"/>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">
            <xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>*:</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>[namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="preceding"
                    select="count(preceding-sibling::*[local-name()=local-name(current())                                   and namespace-uri() = namespace-uri(current())])"/>
      <xsl:text>[</xsl:text>
      <xsl:value-of select="1+ $preceding"/>
      <xsl:text>]</xsl:text>
   </xsl:template>
   <xsl:template match="@*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">@<xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>@*[local-name()='</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>' and namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-2-->
   <!--This mode can be used to generate prefixed XPath for humans-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-2">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="preceding-sibling::*[name(.)=name(current())]">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-3-->
   <!--This mode can be used to generate prefixed XPath for humans 
	(Top-level element has index)-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-3">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="parent::*">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: GENERATE-ID-FROM-PATH -->
   <xsl:template match="/" mode="generate-id-from-path"/>
   <xsl:template match="text()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.text-', 1+count(preceding-sibling::text()), '-')"/>
   </xsl:template>
   <xsl:template match="comment()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.comment-', 1+count(preceding-sibling::comment()), '-')"/>
   </xsl:template>
   <xsl:template match="processing-instruction()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.processing-instruction-', 1+count(preceding-sibling::processing-instruction()), '-')"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.@', name())"/>
   </xsl:template>
   <xsl:template match="*" mode="generate-id-from-path" priority="-0.5">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:text>.</xsl:text>
      <xsl:value-of select="concat('.',name(),'-',1+count(preceding-sibling::*[name()=name(current())]),'-')"/>
   </xsl:template>
   <!--MODE: GENERATE-ID-2 -->
   <xsl:template match="/" mode="generate-id-2">U</xsl:template>
   <xsl:template match="*" mode="generate-id-2" priority="2">
      <xsl:text>U</xsl:text>
      <xsl:number level="multiple" count="*"/>
   </xsl:template>
   <xsl:template match="node()" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>n</xsl:text>
      <xsl:number count="node()"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="string-length(local-name(.))"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="translate(name(),':','.')"/>
   </xsl:template>
   <!--Strip characters-->
   <xsl:template match="text()" priority="-1"/>
   <!--SCHEMA SETUP-->
   <xsl:template match="/">
      <xsl:apply-templates select="/" mode="M4"/>
      <xsl:apply-templates select="/" mode="M5"/>
      <xsl:apply-templates select="/" mode="M6"/>
      <xsl:apply-templates select="/" mode="M7"/>
      <xsl:apply-templates select="/" mode="M10"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M12"/>
      <xsl:apply-templates select="/" mode="M13"/>
      <xsl:apply-templates select="/" mode="M14"/>
      <xsl:apply-templates select="/" mode="M15"/>
      <xsl:apply-templates select="/" mode="M16"/>
      <xsl:apply-templates select="/" mode="M17"/>
      <xsl:apply-templates select="/" mode="M18"/>
      <xsl:apply-templates select="/" mode="M19"/>
      <xsl:apply-templates select="/" mode="M20"/>
      <xsl:apply-templates select="/" mode="M21"/>
      <xsl:apply-templates select="/" mode="M22"/>
      <xsl:apply-templates select="/" mode="M23"/>
      <xsl:apply-templates select="/" mode="M24"/>
      <xsl:apply-templates select="/" mode="M25"/>
      <xsl:apply-templates select="/" mode="M26"/>
      <xsl:apply-templates select="/" mode="M27"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_tekst_024Regelingen - initieel met componentnaam-->
   <!--RULE -->
   <xsl:template match="tekst:BesluitKlassiek/tekst:RegelingKlassiek | tekst:WijzigBijlage/tekst:RegelingCompact | tekst:WijzigBijlage/tekst:RegelingVrijetekst | tekst:WijzigBijlage/tekst:RegelingTijdelijkdeel"
                 priority="1000"
                 mode="M4">
      <xsl:variable name="regeling">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="child::tekst:RegelingOpschrift">
               <xsl:value-of select="string-join(child::tekst:RegelingOpschrift/*/normalize-space(), '')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="string-join(tekst:*/tekst:RegelingOpschrift/*/normalize-space(), '')"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="@componentnaam"/>
         <xsl:otherwise> {"code": "STOP0024", "regeling": "<xsl:text/>
            <xsl:value-of select="$regeling"/>
            <xsl:text/>", "melding": "De initiële regeling \"<xsl:text/>
            <xsl:value-of select="$regeling"/>
            <xsl:text/>\" heeft geen attribuut @componentnaam, dit attribuut is voor een initiële regeling verplicht. Voeg het attribuut toe met een unieke naamgeving.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="@wordt"/>
         <xsl:otherwise> {"code": "STOP0025", "regeling": "<xsl:text/>
            <xsl:value-of select="$regeling"/>
            <xsl:text/>", "melding": "De initiële regeling \"<xsl:text/>
            <xsl:value-of select="$regeling"/>
            <xsl:text/>\" heeft geen attribuut @wordt, dit attribuut is voor een initiële regeling verplicht. Voeg het attribuut toe met als waarde de juiste AKN versie-identifier", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M4"/>
   <xsl:template match="@*|node()" priority="-2" mode="M4">
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <!--PATTERN sch_tekst_031Identificatie - componentnaam uniek-->
   <!--RULE -->
   <xsl:template match="tekst:*[@componentnaam]" priority="1000" mode="M5">
      <xsl:variable name="mijnComponent" select="@componentnaam"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(//tekst:*[@componentnaam = $mijnComponent]) = 1"/>
         <xsl:otherwise> {"code": "STOP0026", "component": "<xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "De componentnaam \"<xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/> binnen <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> is niet uniek. Pas de componentnaam aan om deze uniek te maken", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M5"/>
   <xsl:template match="@*|node()" priority="-2" mode="M5">
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <!--PATTERN sch_tekst_073BesluitCompact WijzigArtikel zonder WijzigLid-->
   <!--RULE -->
   <xsl:template match="tekst:BesluitCompact//tekst:WijzigArtikel[not(ancestor::tekst:RegelingCompact)]"
                 priority="1000"
                 mode="M6">

		<!--REPORT fout-->
      <xsl:if test="child::tekst:WijzigLid">
        {"code": "STOP0073", "id": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het WijzigArtikel <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> heeft een WijzigLid, dit is niet toegestaan binnen een BesluitCompact. Verwijder het WijzigL:id of zet de tekst om naar een element wat.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_tekst_032Identificatie - wordt uniek-->
   <!--RULE -->
   <xsl:template match="tekst:*[@wordt]" priority="1000" mode="M7">
      <xsl:variable name="mijnWordt" select="@wordt"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(//tekst:*[@wordt= $mijnWordt]) = 1"/>
         <xsl:otherwise> 
        {"code": "STOP0074", "wordt": "<xsl:text/>
            <xsl:value-of select="$mijnWordt"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het attribuut @wordt '<xsl:text/>
            <xsl:value-of select="$mijnWordt"/>
            <xsl:text/>' binnen <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> is niet uniek. Pas het attribuut aan om deze uniek te maken (bij een initiele regeling) of (bij mutaties) voeg mutaties samen in één tekst:RegelingMutatie .", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_tekst_012_1Identificatie - eId, wId binnen een AKN-component-->
   <!--RULE -->
   <xsl:template match="tekst:*[@componentnaam]" priority="1000" mode="M10">
      <xsl:variable name="mijnComponent" select="@componentnaam"/>
      <xsl:variable name="eId-fout">
         <xsl:for-each-group xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                             xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                             select=".//tekst:*[@eId]"
                             group-by="@eId">
            <xsl:if test="count(key('alleEIDs',@eId)[ancestor::tekst:*[@componentnaam][1][@componentnaam=$mijnComponent]])&gt;1">
               <xsl:value-of select="./@eId"/>
               <xsl:text>; </xsl:text>
            </xsl:if>
         </xsl:for-each-group>
      </xsl:variable>
      <xsl:variable name="eId-fout-netjes" select="replace($eId-fout,'; $','')"/>
      <xsl:variable name="wId-fout">
         <xsl:for-each-group xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                             xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                             select=".//tekst:*[@wId]"
                             group-by="@wId">
            <xsl:if test="count(key('alleWIDs',@wId)[ancestor::tekst:*[@componentnaam][1][@componentnaam=$mijnComponent]])&gt;1">
               <xsl:value-of select="./@wId"/>
               <xsl:text>; </xsl:text>
            </xsl:if>
         </xsl:for-each-group>
      </xsl:variable>
      <xsl:variable name="wId-fout-netjes" select="replace($wId-fout,'; $','')"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$eId-fout-netjes = ''"/>
         <xsl:otherwise> 
						{"code": "STOP0027", "eId": "<xsl:text/>
            <xsl:value-of select="$eId-fout-netjes"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/>", "melding": "De eId '<xsl:text/>
            <xsl:value-of select="$eId-fout-netjes"/>
            <xsl:text/>' binnen component <xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/> moet uniek zijn. Controleer de opbouw van de eId en corrigeer deze", "ernst": "fout"},
					<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$wId-fout-netjes = ''"/>
         <xsl:otherwise>
						{"code": "STOP0028", "wId": "<xsl:text/>
            <xsl:value-of select="$wId-fout-netjes"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/>", "melding": "De wId '<xsl:text/>
            <xsl:value-of select="$wId-fout-netjes"/>
            <xsl:text/>' binnen component <xsl:text/>
            <xsl:value-of select="$mijnComponent"/>
            <xsl:text/> moet uniek zijn. Controleer de opbouw van de wId en corrigeer deze", "ernst": "fout"},
					<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_tekst_018RegelingMutatie - WijzigInstructies in een WijzigArtikel-->
   <!--RULE -->
   <xsl:template match="tekst:WijzigArtikel//tekst:WijzigInstructies"
                 priority="1000"
                 mode="M11">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:RegelingKlassiek"/>
         <xsl:otherwise> {"code": "STOP0039", "naam": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element WijzigInstructies binnen element <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met eId \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>\" is niet toegestaan. Verwijder de WijzigInstructies, of verplaats deze naar een RegelingMutatie binnen een WijzigBijlage.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_tekst_048RegelingMutatie - OpmerkingVersie in een WijzigArtikel-->
   <!--RULE -->
   <xsl:template match="tekst:WijzigArtikel//tekst:OpmerkingVersie"
                 priority="1000"
                 mode="M12">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:RegelingKlassiek or ancestor::tekst:Rectificatie"/>
         <xsl:otherwise> {"code": "STOP0051", "naam": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element OpmerkingVersie binnen element <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met eId \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>\" is alleen toegestaan in een RegelingKlassiek of Rectificatie daarvan. Verwijder de OpmerkingVersie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_tekst_019RegelingMutatie - in een WijzigArtikel alleen in RegelingKlassiek-->
   <!--RULE -->
   <xsl:template match="tekst:WijzigArtikel//tekst:RegelingMutatie"
                 priority="1000"
                 mode="M13">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:Lichaam/parent::tekst:RegelingKlassiek"/>
         <xsl:otherwise> {"code": "STOP0040", "naam": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element RegelingMutatie binnen element <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met eId \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>\" is niet toegestaan. Neem de RegelingMutatie op in een WijzigBijlage.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0045@Wijzigactie voor Inhoud-->
   <!--RULE -->
   <xsl:template match="tekst:Vervang//tekst:Inhoud[@wijzigactie]"
                 priority="1000"
                 mode="M14">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="parent::tekst:*/tekst:Gereserveerd | parent::tekst:*/tekst:Vervallen | parent::tekst:*/tekst:NogNietInWerking | parent::tekst:*/tekst:Lid"/>
         <xsl:otherwise>{"code": "STOP0063", "naam": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:Vervang[@wat][1])"/>
            <xsl:text/>", "wat": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:Vervang[@wat][1]/@wat"/>
            <xsl:text/>", "melding": "Het element Inhoud van <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:Vervang[@wat][1])"/>
            <xsl:text/> met attribuut @wat \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:Vervang[@wat][1]/@wat"/>
            <xsl:text/>\" heeft ten onrechte een attribuut @wijzigactie. Dit is alleen toegestaan indien gecombineerd met Gereserveerd, Vervallen, NogNietInWerking of Lid (binnen Artikel). Verwijder het attribuut @wijzigactie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_tekst_066-->
   <!--RULE -->
   <xsl:template match="*[@wordt][@was]" priority="1000" mode="M15">
      <xsl:variable name="wasWork" select="substring-before(@was/./string(), '@')"/>
      <xsl:variable name="wordtWork" select="substring-before(@wordt/./string(), '@')"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$wasWork = $wordtWork"/>
         <xsl:otherwise>
      {"code": "STOP0066", "wasID": "<xsl:text/>
            <xsl:value-of select="$wasWork"/>
            <xsl:text/>", "wordtID": "<xsl:text/>
            <xsl:value-of select="$wordtWork"/>
            <xsl:text/>", "melding": "De identificatie van de @was <xsl:text/>
            <xsl:value-of select="$wasWork"/>
            <xsl:text/> en @wordt <xsl:text/>
            <xsl:value-of select="$wordtWork"/>
            <xsl:text/> hebben niet dezelfde work-identificatie. Corrigeer de AKN-expression identificatie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <!--PATTERN sch_tekst_068Noot unieke ids-->
   <!--RULE -->
   <xsl:template match="tekst:*[@componentnaam]" priority="1000" mode="M16">
      <xsl:variable name="component" select="@componentnaam"/>
      <xsl:variable name="nootIndex">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="//tekst:Noot[ancestor::tekst:*[@componentnaam][1][@componentnaam = $component]][not(ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'])][not(ancestor::tekst:Verwijder)]">
            <xsl:sort select="@id"/>
            <n>
               <xsl:value-of select="@id"/>
            </n>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="nootId-fout">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$nootIndex/n[preceding-sibling::n = .]">
            <xsl:value-of select="self::n/."/>
            <xsl:if test="not(position() = last())">
               <xsl:text>; </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$nootId-fout = ''"/>
         <xsl:otherwise>
      {"code": "STOP0067", "id": "<xsl:text/>
            <xsl:value-of select="$nootId-fout"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="$component"/>
            <xsl:text/>", "melding": "De id voor tekst:Noot '<xsl:text/>
            <xsl:value-of select="$nootId-fout"/>
            <xsl:text/>' binnen component '<xsl:text/>
            <xsl:value-of select="$component"/>
            <xsl:text/>' moet uniek zijn. Controleer de id en corrigeer zodat de identificatie uniek is binnen de component.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M16"/>
   <xsl:template match="@*|node()" priority="-2" mode="M16">
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0077Wat moet overeenkomen met wId-->
   <!--RULE -->
   <xsl:template match="tekst:Vervang | tekst:Verwijder" priority="1000" mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="@wat = child::tekst:*[@wId][1]/@wId"/>
         <xsl:otherwise>
  {"code": "STOP0077", "watID": "<xsl:text/>
            <xsl:value-of select="@wat"/>
            <xsl:text/>", "wId": "<xsl:text/>
            <xsl:value-of select="child::tekst:*[@wId][1]/@wId"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/>", "melding": "De identificatie in attribuut @wat \"<xsl:text/>
            <xsl:value-of select="@wat"/>
            <xsl:text/>\" in het in element <xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/> is niet gelijk aan de wId \"<xsl:text/>
            <xsl:value-of select="child::tekst:*[@wId][1]/@wId"/>
            <xsl:text/>\" van het element dat verwijderd of vervangen wordt", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M17"/>
   <xsl:template match="@*|node()" priority="-2" mode="M17">
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0080-->
   <!--RULE -->
   <xsl:template match="tekst:WijzigArtikel[ancestor::tekst:RegelingMutatie]"
                 priority="1000"
                 mode="M18">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:Rectificatie"/>
         <xsl:otherwise>
     {"code": "STOP0080", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "Het element WijzigArtikel met <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> mag alleen worden gebruikt in een RegelingMutatie binnen een Rectificatie. Verwijder het WijzigArtikel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M18"/>
   <xsl:template match="@*|node()" priority="-2" mode="M18">
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0086Renvooi verplicht in Vervang/VervangKop-->
   <!--RULE -->
   <xsl:template match="tekst:Vervang|tekst:VervangKop" priority="1000" mode="M19">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="exists(@context) or @revisie/string() = '1' or .//tekst:NieuweTekst or .//tekst:VerwijderdeTekst or .//tekst:*[@wijzigactie]"/>
         <xsl:otherwise>
        {"code": "STOP0086", "element": "<xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/>", "wat": "<xsl:text/>
            <xsl:value-of select="@wat/string()"/>
            <xsl:text/>", "parent": "<xsl:text/>
            <xsl:value-of select="local-name(..)"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="../@componentnaam/string()"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/>(@wat='<xsl:text/>
            <xsl:value-of select="@wat/string()"/>
            <xsl:text/>') binnen <xsl:text/>
            <xsl:value-of select="local-name(..)"/>
            <xsl:text/>(@componentnaam='<xsl:text/>
            <xsl:value-of select="../@componentnaam/string()"/>
            <xsl:text/>') bevat geen renvooimarkering. Dit is niet toegestaan. Voeg tekst:NieuweTekst, tekst:VerwijderdeTekst of het attribuut wijzigactie toe op de plaats van de tekstwijziging binnen <xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M19"/>
   <xsl:template match="@*|node()" priority="-2" mode="M19">
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0118geen renvooi in renvooi-->
   <!--RULE -->
   <xsl:template match="tekst:NieuweTekst | tekst:VerwijderdeTekst"
                 priority="1000"
                 mode="M20">

		<!--REPORT fout-->
      <xsl:if test="ancestor::tekst:NieuweTekst or ancestor::tekst:VerwijderdeTekst"> {"code": "STOP0118", "element": "<xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/>", "parent": "<xsl:text/>
         <xsl:value-of select="node-name((ancestor::tekst:NieuweTekst[1] | ancestor::tekst:VerwijderdeTekst[1])[1])"/>
         <xsl:text/>", "fragment": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "fragment-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/> staat binnen <xsl:text/>
         <xsl:value-of select="node-name((ancestor::tekst:NieuweTekst[1] | ancestor::tekst:VerwijderdeTekst[1])[1])"/>
         <xsl:text/> in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>(<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>). Dit is niet toegestaan. Verwijder het renvooi-element uit de wijziging.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M20"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M20"/>
   <xsl:template match="@*|node()" priority="-2" mode="M20">
      <xsl:apply-templates select="*" mode="M20"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0119@context en @positie altijd samen-->
   <!--RULE -->
   <xsl:template match="tekst:Vervang" priority="1000" mode="M21">
      <xsl:variable name="ontbrekend">
         <xsl:if xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="(empty(@positie) and @context) or (@positie and empty(@context))">
            <xsl:if test="empty(@positie)">positie</xsl:if>
            <xsl:if test="empty(@context)">context</xsl:if>
         </xsl:if>
      </xsl:variable>
      <xsl:variable name="element">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="child::tekst:*">
            <xsl:choose>
               <xsl:when test="matches(local-name(), 'Wat')"/>
               <xsl:when test="matches(local-name(), 'Nummer')"/>
               <xsl:otherwise>
                  <xsl:value-of select="local-name()"/>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--REPORT fout-->
      <xsl:if test="(not(@context) and @positie) or (not(@positie) and @context)"> {"code": "STOP0119", "element": "<xsl:text/>
         <xsl:value-of select="$element"/>
         <xsl:text/>", "ontbrekendattribuut": "<xsl:text/>
         <xsl:value-of select="$ontbrekend"/>
         <xsl:text/>", "attribuut": "<xsl:text/>
         <xsl:value-of select="concat(node-name(@context), node-name(@positie))"/>
         <xsl:text/>", "wId": "<xsl:text/>
         <xsl:value-of select="child::tekst:*/@wId"/>
         <xsl:text/>", "melding": "Het attribuut <xsl:text/>
         <xsl:value-of select="concat(node-name(@context), node-name(@positie))"/>
         <xsl:text/> komt voor op tekst:Vervang van <xsl:text/>
         <xsl:value-of select="$element"/>
         <xsl:text/>(<xsl:text/>
         <xsl:value-of select="child::tekst:*/@wId"/>
         <xsl:text/>) terwijl attribuut <xsl:text/>
         <xsl:value-of select="$ontbrekend"/>
         <xsl:text/> ontbreekt. Dit is niet toegestaan. Voeg attribuut <xsl:text/>
         <xsl:value-of select="$ontbrekend"/>
         <xsl:text/> toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M21"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M21"/>
   <xsl:template match="@*|node()" priority="-2" mode="M21">
      <xsl:apply-templates select="*" mode="M21"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0122Redactioneel niet in besluitcompact-->
   <!--RULE -->
   <xsl:template match="tekst:BesluitCompact/tekst:Lichaam//tekst:Redactioneel"
                 priority="1000"
                 mode="M22">

		<!--REPORT fout-->
      <xsl:if test="."> {"code": "STOP0122", "element": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element Redactioneel binnen <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>(<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>) staat in het besluitdeel van het Besluit. Dit is niet toegestaan. Verwijder het element Redactioneel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M22"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M22"/>
   <xsl:template match="@*|node()" priority="-2" mode="M22">
      <xsl:apply-templates select="*" mode="M22"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0123@context/@positie uniek-->
   <!--RULE -->
   <xsl:template match="tekst:*[@context][@positie]" priority="1000" mode="M23">
      <xsl:variable name="mijnContext" select="@context"/>
      <xsl:variable name="mijnPositie" select="@positie"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(../tekst:*[@context = $mijnContext][@positie = $mijnPositie]) = 1"/>
         <xsl:otherwise> 
        {"code": "STOP0123", "element": "<xsl:text/>
            <xsl:value-of select="node-name(.)"/>
            <xsl:text/>", "context": "<xsl:text/>
            <xsl:value-of select="$mijnContext"/>
            <xsl:text/>", "positie": "<xsl:text/>
            <xsl:value-of select="$mijnPositie"/>
            <xsl:text/>", "melding": "De combinatie van attributen @context=\"<xsl:text/>
            <xsl:value-of select="$mijnContext"/>
            <xsl:text/>\" en @positie=\"<xsl:text/>
            <xsl:value-of select="$mijnPositie"/>
            <xsl:text/>\" op element <xsl:text/>
            <xsl:value-of select="node-name(.)"/>
            <xsl:text/> is niet uniek. Hierdoor kent de RegelingMutatie geen eenduidige interpretatie. Maak elke combinatie van @positie en @context binnen RegelingMutatie uniek.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M23"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M23"/>
   <xsl:template match="@*|node()" priority="-2" mode="M23">
      <xsl:apply-templates select="*" mode="M23"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0124verwijderd element niet gebruiken als @context-->
   <!--RULE -->
   <xsl:template match="tekst:*[@context]" priority="1000" mode="M24">
      <xsl:variable name="mijnwId" select="@context"/>
      <!--REPORT fout-->
      <xsl:if test="../tekst:Verwijder[@wat = $mijnwId] or ..//tekst:*[@wId = $mijnwId][@wijzigactie='verwijder'] or ..//tekst:*[@wId = $mijnwId][ancestor::tekst:Verwijder] or ..//tekst:*[@wId = $mijnwId][ancestor::tekst:*[@wijzigactie='verwijder']]"> 
        {"code": "STOP0124", "element": "<xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/>", "wId": "<xsl:text/>
         <xsl:value-of select="$mijnwId"/>
         <xsl:text/>", "melding": "Het te verwijderen element met wId <xsl:text/>
         <xsl:value-of select="$mijnwId"/>
         <xsl:text/> wordt als @context gebruikt op element <xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/>. Dit is niet toegestaan. Gebruik de wId van een element dat niet verwijderd wordt als @context.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M24"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M24"/>
   <xsl:template match="@*|node()" priority="-2" mode="M24">
      <xsl:apply-templates select="*" mode="M24"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0126Alleen @wijzigactie verwijderContainer op element dat zelf vervangen wordt-->
   <!--RULE -->
   <xsl:template match="tekst:Vervang/tekst:*[@wijzigactie] "
                 priority="1000"
                 mode="M25">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(@wijzigactie/string(), '^verwijderContainer$') or matches(local-name(.), '^Nummer$')"/>
         <xsl:otherwise> 
        {"code": "STOP0126", "mutatie-element": "<xsl:text/>
            <xsl:value-of select="node-name(..)"/>
            <xsl:text/>", "wat": "<xsl:text/>
            <xsl:value-of select="../@wat"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="node-name(.)"/>
            <xsl:text/>", "actie": "<xsl:text/>
            <xsl:value-of select="@wijzigactie"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="node-name(..)"/>
            <xsl:text/>(wat=<xsl:text/>
            <xsl:value-of select="../@wat"/>
            <xsl:text/>) vervangt element <xsl:text/>
            <xsl:value-of select="node-name(.)"/>
            <xsl:text/> met wijzigactie=\"<xsl:text/>
            <xsl:value-of select="@wijzigactie"/>
            <xsl:text/>\". Deze wijzigactie is hier niet toegestaan. Verwijder het attribuut wijzigactie of wijzig het in verwijderContainer.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M25"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M25"/>
   <xsl:template match="@*|node()" priority="-2" mode="M25">
      <xsl:apply-templates select="*" mode="M25"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0127Geen @wijzigactie op Nummer binnen Vervang-->
   <!--RULE -->
   <xsl:template match="tekst:Nummer[@wijzigactie][parent::tekst:Vervang|parent::tekst:VervangKop]"
                 priority="1000"
                 mode="M26">

		<!--REPORT fout-->
      <xsl:if test="."> 
        {"code": "STOP0127", "element": "<xsl:text/>
         <xsl:value-of select="node-name(..)"/>
         <xsl:text/>", "actie": "<xsl:text/>
         <xsl:value-of select="@wijzigactie"/>
         <xsl:text/>", "wat": "<xsl:text/>
         <xsl:value-of select="../@wat"/>
         <xsl:text/>", "melding": "Het element Nummer binnen <xsl:text/>
         <xsl:value-of select="node-name(..)"/>
         <xsl:text/>(@wat=\"<xsl:text/>
         <xsl:value-of select="../@wat"/>
         <xsl:text/>\") heeft een attribuut wijzigactie=\"<xsl:text/>
         <xsl:value-of select="@wijzigactie"/>
         <xsl:text/>\". Het attribuut wijzigactie is hier niet toegestaan. Verwijder het attribuut wijzigactie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M26"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M26"/>
   <xsl:template match="@*|node()" priority="-2" mode="M26">
      <xsl:apply-templates select="*" mode="M26"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0128Renvooi niet toegestaan in Vervang als @revisie = '1' aanwezig-->
   <!--RULE STOP0128-->
   <xsl:template match="tekst:Vervang[@revisie = 1]" priority="1000" mode="M27">

		<!--REPORT fout-->
      <xsl:if test=".//tekst:NieuweTekst or .//tekst:VerwijderdeTekst or .//tekst:*[@wijzigactie] or exists(@context)">
        {"code": "STOP0128", "element": "<xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>", "wat": "<xsl:text/>
         <xsl:value-of select="@wat/string()"/>
         <xsl:text/>", "parent": "<xsl:text/>
         <xsl:value-of select="local-name(..)"/>
         <xsl:text/>", "component": "<xsl:text/>
         <xsl:value-of select="../@componentnaam/string()"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>(@wat='<xsl:text/>
         <xsl:value-of select="@wat/string()"/>
         <xsl:text/>') binnen <xsl:text/>
         <xsl:value-of select="local-name(..)"/>
         <xsl:text/>(@componentnaam='<xsl:text/>
         <xsl:value-of select="../@componentnaam/string()"/>
         <xsl:text/>') bevat een verplaatsing en/of een renvooimarkering terwijl het een niet-juridische wijziging betreft (@revisie='1'). Dit is niet toegestaan. Verwijder het attribuut @revisie='1', maak de verplaatsing ongedaan ( verwijder @context en @positie) of verwijder de renvooi (tekst:NieuweTekst, tekst:VerwijderdeTekst, attribuut @wijzigactie binnen <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M27"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M27"/>
   <xsl:template match="@*|node()" priority="-2" mode="M27">
      <xsl:apply-templates select="*" mode="M27"/>
   </xsl:template>
</xsl:stylesheet>
