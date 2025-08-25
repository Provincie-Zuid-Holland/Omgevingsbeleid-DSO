<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
                xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
                xmlns:gio="https://standaarden.overheid.nl/stop/imop/gio/"
                xmlns:cons="https://standaarden.overheid.nl/stop/imop/consolidatie/"
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
      <xsl:apply-templates select="/" mode="M8"/>
      <xsl:apply-templates select="/" mode="M9"/>
      <xsl:apply-templates select="/" mode="M10"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M12"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_data_001Generieke AKN en JOIN validaties-->
   <!--RULE -->
   <xsl:template match="*:FRBRWork | *:FRBRExpression | *:instrumentVersie | *:instrument | *:doel | tekst:ExtIoRef | data:opvolgerVan | data:heeftGeboorteregeling | data:informatieobjectRef | data:mededelingOver | cons:publiceert | data:publiceert | gio:contextGIOs | geo:wasID | cons:heeftTijdelijkDeel | tekst:ExtRef[@soort = 'AKN'][matches(@ref, '^/akn/(nl|aw|cw|sx)/')] | tekst:ExtRef[@soort = 'JOIN']"
                 priority="1000"
                 mode="M8">
      <xsl:variable name="taalexpressie" select="'^(nld|eng|fry|pap|mul|und)$'"/>
      <xsl:variable name="landexpressie" select="'^(nl|aw|cw|sx)$'"/>
      <xsl:variable name="AKNexpressie" select="'^(bill|act|doc|officialGazette)$'"/>
      <xsl:variable name="JOINexpressie"
                    select="'^(pubdata|regdata|infodata|proces|versie)$'"/>
      <xsl:variable name="Consolidatieexpressie"
                    select="'^(land|provincie|gemeente|waterschap|consolidatie)$'"/>
      <xsl:variable name="BGexpressie"
                    select="'^(mnre\d{4}|mn\d{3}|gm\d{4}|ws\d{4}|pv\d{2})$'"/>
      <xsl:variable name="Identificatie">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="string(local-name(.)) = 'ExtRef'">
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
      </xsl:variable>
      <xsl:variable name="Identificatie_reeks" select="tokenize($Identificatie, '/')"/>
      <xsl:variable name="Identificatie_deel1" select="$Identificatie_reeks[2]"/>
      <xsl:variable name="isAKN" select="starts-with($Identificatie, '/akn/')"/>
      <xsl:variable name="isJOIN" select="starts-with($Identificatie, '/join/')"/>
      <xsl:variable name="Identificatie_deel2" select="$Identificatie_reeks[3]"/>
      <xsl:variable name="Identificatie_deel3" select="$Identificatie_reeks[4]"/>
      <xsl:variable name="IsPublicatie" select="$Identificatie_deel3 = 'officialGazette'"/>
      <xsl:variable name="IsDoel" select="$Identificatie_deel3 = 'proces'"/>
      <xsl:variable name="IsAct" select="$Identificatie_deel3 = 'act'"/>
      <xsl:variable name="AKNValide" select="matches($Identificatie_deel3, $AKNexpressie)"/>
      <xsl:variable name="JOINValide"
                    select="matches($Identificatie_deel3, $JOINexpressie)"/>
      <xsl:variable name="Identificatie_deel4" select="$Identificatie_reeks[5]"/>
      <xsl:variable name="IsConsolidatie"
                    select="matches($Identificatie_deel4, $Consolidatieexpressie)"/>
      <xsl:variable name="IsBRPcode" select="matches($Identificatie_deel4, $BGexpressie)"/>
      <xsl:variable name="Identificatie_deel5" select="$Identificatie_reeks[6]"/>
      <xsl:variable name="Identificatie_deel6" select="$Identificatie_reeks[7]"/>
      <xsl:variable name="Identificatie_deel7" select="$Identificatie_reeks[8]"/>
      <xsl:variable name="Identificatie_rest"
                    select="substring-after($Identificatie, concat($Identificatie_deel6, '/', $Identificatie_deel7))"/>
      <xsl:variable name="IsExpressie"
                    select="exists($Identificatie_deel7) and contains($Identificatie_deel7, '@')"/>
      <xsl:variable name="Expressie_datum">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="contains($Identificatie_deel7, ';')">
               <xsl:value-of select="substring-before(substring-after($Identificatie_deel7, '@'), ';')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="substring-after($Identificatie_deel7, '@')"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--REPORT fout-->
      <xsl:if test="contains($Identificatie, '.')">
        {"code": "STOP1000", "ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "De identifier <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> bevat een punt. Dit is niet toegestaan. Verwijder de punt.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$isAKN or $isJOIN"/>
         <xsl:otherwise>
        {"code": "STOP1014", "ID": "<xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/>", "melding": "De waarde <xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/> begint niet met /akn/ of /join/. Pas de waarde aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="$isAKN and not(matches($Identificatie_deel2, $landexpressie))">
	    {"code": "STOP1002", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Identificatie_deel2"/>
         <xsl:text/>", "melding": "Landcode <xsl:text/>
         <xsl:value-of select="$Identificatie_deel2"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> is niet toegestaan. Pas landcode aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$isJOIN and not(matches($Identificatie_deel2, '^(id)$'))">
	    {"code": "STOP1003", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "Tweede deel JOIN-identificatie <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> moet gelijk zijn aan 'id'. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$isJOIN and not($JOINValide)">
	  	{"code": "STOP1004", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "Derde deel JOIN-identificatie <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> moet gelijk zijn aan 'regdata', 'pubdata', 'infodata' voor verwijzing naar een informatieobject of 'proces' voor een doel. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$isAKN and not($AKNValide)">
	  	{"code": "STOP2081", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "Derde deel AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> moet gelijk zijn aan 'bill', 'act', 'doc' voor verwijzing naar een besluit, regeling, overige te publiceren documenten of 'officialGazette' voor een gepubliceerd document. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="($AKNValide or $JOINValide) and not($IsPublicatie or $IsBRPcode or $IsConsolidatie)">
		  {"code": "STOP1010", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Identificatie_deel4"/>
         <xsl:text/>", "melding": "Vierde deel van AKN/JOIN (<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>) moet gelijk zijn aan een brp-code, een code voor geconsolidatieolideerde instrumenten of 'proces' voor een doel. Pas (<xsl:text/>
         <xsl:value-of select="$Identificatie_deel4"/>
         <xsl:text/>) aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($Identificatie_deel5 castable as xs:date and string-length($Identificatie_deel5) = 10) or ($Identificatie_deel5 castable as xs:gYear and string-length($Identificatie_deel5) = 4)"/>
         <xsl:otherwise>
		  {"code": "STOP1006", "Work-ID": "<xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/>", "melding": "Vijfde deel AKN- of JOIN-identificatie <xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/> moet gelijk zijn aan jaartal of geldige datum. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="not($IsExpressie) and ($Identificatie_deel7 != '' or $Identificatie_rest != '')">
		  {"code": "STOP2078", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "De identifier <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> bestaat niet uit minimaal zes door een '/' gescheiden delen. Dit is niet toegestaan. Geef de identifier het correcte formaat.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($Identificatie_deel6, '^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$')"/>
         <xsl:otherwise>
		  {"code": "STOP2079", "Work-ID": "<xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/>", "substring": "<xsl:text/>
            <xsl:value-of select="$Identificatie_deel6"/>
            <xsl:text/>", "melding": "De identifier <xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/> heeft geen correcte 'overig'-aanduiding <xsl:text/>
            <xsl:value-of select="$Identificatie_deel6"/>
            <xsl:text/>. Dit deel begint niet met een letter of cijfer en/of bevat ook andere tekens dan letters, cijfers, '_' en '-'. Corrigeer de identifier.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="$IsExpressie and $Identificatie_rest != ''">
		  {"code": "STOP2080", "Expression-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "TeLang": "<xsl:text/>
         <xsl:value-of select="$Identificatie_rest"/>
         <xsl:text/>", "melding": "De expressie-identifier <xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/> bestaat uit meer dan zeven delen gescheiden door een '/'. <xsl:text/>
         <xsl:value-of select="$Identificatie_rest"/>
         <xsl:text/> is overbodig. Corrigeer de expressie-identifier.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not($IsExpressie) or matches(substring-before($Identificatie_deel7, '@'), $taalexpressie)"/>
         <xsl:otherwise>
		  {"code": "STOP1009", "Expression-ID": "<xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/>", "substring": "<xsl:text/>
            <xsl:value-of select="substring-before($Identificatie_deel7, '@')"/>
            <xsl:text/>", "melding": "Voor een AKN- of JOIN-identificatie (<xsl:text/>
            <xsl:value-of select="$Identificatie"/>
            <xsl:text/>) moet het deel voorafgaand aan de '@' (<xsl:text/>
            <xsl:value-of select="substring-before($Identificatie_deel7, '@')"/>
            <xsl:text/>) een geldige taal zijn ('nld','eng','fry','pap','mul','und'). Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="$IsExpressie and (not($IsAct) or $IsConsolidatie) and not(($Expressie_datum castable as xs:date and (string-length($Expressie_datum) = 10)) or ($Expressie_datum castable as xs:gYear and (string-length($Expressie_datum) = 4)))">
		  {"code": "STOP1007", "Expression-ID": "<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>", "melding": "Voor een AKN- of JOIN-identificatie (<xsl:text/>
         <xsl:value-of select="$Identificatie"/>
         <xsl:text/>) moet het eerste deel na de '@' een jaartal of een geldige datum zijn. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_data_002ExpressionID begint met WorkID-->
   <!--RULE -->
   <xsl:template match="*:ExpressionIdentificatie | geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie"
                 priority="1000"
                 mode="M9">
      <xsl:variable name="Work" select="normalize-space(*:FRBRWork)"/>
      <xsl:variable name="Expression" select="normalize-space(*:FRBRExpression)"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="starts-with($Expression, concat($Work, '/'))"/>
         <xsl:otherwise>
        {"code": "STOP1001", "Work-ID": "<xsl:text/>
            <xsl:value-of select="$Work"/>
            <xsl:text/>", "Expression-ID": "<xsl:text/>
            <xsl:value-of select="$Expression"/>
            <xsl:text/>", "melding": "Het gedeelte van de FRBRExpression <xsl:text/>
            <xsl:value-of select="$Expression"/>
            <xsl:text/> vóór de 'taalcode/@' is niet gelijk aan de FRBRWork-identificatie <xsl:text/>
            <xsl:value-of select="$Work"/>
            <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_data_005AKN/JOIN validaties Expression/Work icm soortWork in
      ExpressionIdentificatie-->
   <!--RULE -->
   <xsl:template match="*:ExpressionIdentificatie" priority="1000" mode="M10">
      <xsl:variable name="soortWork" select="normalize-space(./*:soortWork/string())"/>
      <xsl:variable name="Expression" select="normalize-space(./*:FRBRExpression/string())"/>
      <xsl:variable name="Work" select="normalize-space(./*:FRBRWork/string())"/>
      <xsl:variable name="Expression_reeks" select="tokenize($Expression, '/')"/>
      <xsl:variable name="Expression_datum_work" select="$Expression_reeks[6]"/>
      <xsl:variable name="Expression_restdeel" select="$Expression_reeks[8]"/>
      <xsl:variable name="Expression_restdeel_reeks"
                    select="tokenize($Expression_restdeel, '@')"/>
      <xsl:variable name="Expression_restdeel_deel2" select="$Expression_restdeel_reeks[2]"/>
      <xsl:variable name="Expression_restdeel_deel2_reeks"
                    select="tokenize($Expression_restdeel_deel2, ';')"/>
      <xsl:variable name="Expression_datum_expr"
                    select="$Expression_restdeel_deel2_reeks[1]"/>
      <xsl:variable name="Work_reeks" select="tokenize($Work, '/')"/>
      <xsl:variable name="Work_objecttype" select="$Work_reeks[3]"/>
      <xsl:variable name="Work_collectie" select="$Work_reeks[4]"/>
      <xsl:variable name="Work_documenttype" select="$Work_reeks[4]"/>
      <xsl:variable name="Work_overheid" select="$Work_reeks[5]"/>
      <xsl:variable name="is_besluit" select="$soortWork = '/join/id/stop/work_003'"/>
      <xsl:variable name="is_kennisgeving" select="$soortWork = '/join/id/stop/work_023'"/>
      <xsl:variable name="is_mededeling" select="$soortWork = '/join/id/stop/work_025'"/>
      <xsl:variable name="is_rectificatie" select="$soortWork = '/join/id/stop/work_018'"/>
      <xsl:variable name="is_tijdelijkregelingdeel"
                    select="$soortWork = '/join/id/stop/work_021'"/>
      <xsl:variable name="is_regeling"
                    select="$soortWork = '/join/id/stop/work_019' or $soortWork = '/join/id/stop/work_006' or $soortWork = '/join/id/stop/work_021' or $soortWork = '/join/id/stop/work_022'"/>
      <xsl:variable name="is_publicatie" select="$soortWork = '/join/id/stop/work_015'"/>
      <xsl:variable name="is_informatieobject"
                    select="$soortWork = '/join/id/stop/work_010'"/>
      <xsl:variable name="is_cons_informatieobject"
                    select="$soortWork = '/join/id/stop/work_005'"/>
      <xsl:variable name="bladcode" select="'^(bgr|gmb|prb|stb|stcrt|trb|wsb)$'"/>
      <xsl:variable name="is_join" select="$is_informatieobject"/>
      <xsl:variable name="is_akn"
                    select="$is_besluit or $is_publicatie or $is_regeling or $is_kennisgeving or $is_rectificatie or $is_mededeling"/>
      <!--REPORT fout-->
      <xsl:if test="$is_publicatie and not(matches($Work_documenttype, '^officialGazette$'))">
	    {"code": "STOP1011", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/>", "melding": "Derde veld <xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/> is niet toegestaan bij officiele publicatie. Pas dit veld aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$is_besluit and not(matches($Work_documenttype, '^bill$'))">
	    {"code": "STOP1013", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/>", "melding": "Derde veld <xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/> is niet toegestaan bij besluit. Pas dit veld aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$is_regeling and not(matches($Work_documenttype, '^act$'))">
	    {"code": "STOP1012", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/>", "melding": "Derde veld <xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/> is niet toegestaan bij regeling. Pas dit veld aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$is_join and not($Expression_datum_expr &gt;= $Expression_datum_work)"> 
		  {"code": "STOP1008", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "Expression-ID": "<xsl:text/>
         <xsl:value-of select="$Expression"/>
         <xsl:text/>", "melding": "JOIN-identificatie (<xsl:text/>
         <xsl:value-of select="$Expression"/>
         <xsl:text/>) MOET als eerste deel na de '@' een jaartal of een geldige datum hebben groter/gelijk aan jaartal in werk (<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>). Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="($is_kennisgeving or $is_mededeling) and not(matches($Work_documenttype, '^doc$'))">
	    {"code": "STOP1037", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/>", "melding": "Derde veld <xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/> is niet toegestaan voor een kennisgeving of mededeling. Pas dit veld aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$is_rectificatie and not(matches($Work_documenttype, '^doc$'))">
	    {"code": "STOP1044", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "substring": "<xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/>", "melding": "Derde deel <xsl:text/>
         <xsl:value-of select="$Work_documenttype"/>
         <xsl:text/> in de AKN-identificatie <xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/> is niet toegestaan voor een rectificatie. Pas dit deel aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="matches($Work_documenttype, '^bill$') and not($is_besluit)">
	    {"code": "STOP2002", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "soortWork": "<xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>", "melding": "FRBRWork '<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>' begint met '/akn/nl/bill/' maar soortwork'<xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>' is niet gelijk aan '/join/id/stop/work_003'(besluit).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="matches($Work_documenttype, '^act$') and not($is_regeling)">
	    {"code": "STOP2003", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "soortWork": "<xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>", "melding": "FRBRWork '<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>' begint met '/akn/nl/act/' maar soortwork <xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>' is niet gelijk aan '/join/id/stop/work_019'(Regeling), '/join/id/stop/work_006'(Geconsolideerde regeling), '/join/id/stop/work_021'(Tijdelijk regelingdeel) of '/join/id/stop/work_022'(Consolidatie van tijdelijk regelingdeel).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="matches($Work_documenttype, '^doc$') and not($is_rectificatie or $is_kennisgeving or $is_mededeling)">
	    {"code": "STOP2052", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "soortWork": "<xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>", "melding": "FRBRWork '<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>' begint met '/akn/nl/doc/' maar soortwork <xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>' is niet gelijk aan '/join/id/stop/work_018'(rectificatie), '/join/id/stop/work_023'(kennisgeving) of '/join/id/stop/work_025'(mededeling).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="(matches($Work_objecttype, '^id$')) and not($is_informatieobject or $is_cons_informatieobject)">
	    {"code": "STOP2024", "Work-ID": "<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>", "soortWork": "<xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>", "melding": "FRBRWork '<xsl:text/>
         <xsl:value-of select="$Work"/>
         <xsl:text/>' begint met '/join/id' maar soortwork <xsl:text/>
         <xsl:value-of select="$soortWork"/>
         <xsl:text/>' is niet gelijk aan '/join/id/stop/work_010'(informatieobject) of '/join/id/stop/work_005'(geconsolideerd informatieobject).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_data_058-->
   <!--RULE -->
   <xsl:template match="data:ExpressionIdentificatie[data:soortWork = '/join/id/stop/work_021']"
                 priority="1000"
                 mode="M11">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="child::data:isTijdelijkDeelVan"/>
         <xsl:otherwise>
	    {"code": "STOP2058", "Work-ID": "<xsl:text/>
            <xsl:value-of select="data:FRBRWork"/>
            <xsl:text/>", "melding": "De ExpressionIdentificatie('<xsl:text/>
            <xsl:value-of select="data:FRBRWork"/>
            <xsl:text/>') is van een tijdelijk regelingdeel (data:soortWork = '/join/id/stop/work_021') maar deze geeft niet aan van welke regeling het een tijdelijk deel is. Voeg data:isTijdelijkDeelVan toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_data_006Tijdelijk regelingdeel-->
   <!--RULE -->
   <xsl:template match="data:isTijdelijkDeelVan" priority="1000" mode="M12">
      <xsl:variable name="soortWorkTijdelijkdeel"
                    select="parent::data:ExpressionIdentificatie/data:soortWork/string()"/>
      <xsl:variable name="workTijdelijkdeel"
                    select="parent::data:ExpressionIdentificatie/data:FRBRWork/string()"/>
      <xsl:variable name="workTijdelijkdeel_reeks"
                    select="tokenize($workTijdelijkdeel, '/')"/>
      <xsl:variable name="workTijdelijkDeel_documenttype"
                    select="$workTijdelijkdeel_reeks[4]"/>
      <xsl:variable name="soortWorkVanRegeling"
                    select="data:WorkIdentificatie/data:soortWork/string()"/>
      <xsl:variable name="workVanRegeling"
                    select="data:WorkIdentificatie/data:FRBRWork/string()"/>
      <xsl:variable name="workVanRegeling_reeks" select="tokenize($workVanRegeling, '/')"/>
      <xsl:variable name="workVanRegeling_documenttype" select="$workVanRegeling_reeks[4]"/>
      <xsl:variable name="is_tijdelijkregelingdeel"
                    select="$soortWorkTijdelijkdeel = '/join/id/stop/work_021'"/>
      <xsl:variable name="is_regeling"
                    select="$soortWorkVanRegeling = '/join/id/stop/work_019'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$is_tijdelijkregelingdeel"/>
         <xsl:otherwise>
        {"code": "STOP2004", "soortWork": "<xsl:text/>
            <xsl:value-of select="$soortWorkTijdelijkdeel"/>
            <xsl:text/>", "melding": "De ExpressionIdentificatie bevat data:isTijdelijkDeelVan, maar data:soortWork('<xsl:text/>
            <xsl:value-of select="$soortWorkTijdelijkdeel"/>
            <xsl:text/>') is niet gelijk aan '/join/id/stop/work_021'(tijdelijk regelingdeel). Pas soortWork aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$is_regeling"/>
         <xsl:otherwise>
        {"code": "STOP2057", "soortWork": "<xsl:text/>
            <xsl:value-of select="$soortWorkVanRegeling"/>
            <xsl:text/>", "melding": "De ExpressionIdentificatie bevat data:isTijdelijkDeelVan, maar het soortWork('<xsl:text/>
            <xsl:value-of select="$soortWorkVanRegeling"/>
            <xsl:text/>') van de regeling waar deze regeling een tijdelijk deel van is, is niet gelijk aan '/join/id/stop/work_019' (regeling). Pas soortWork aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$workVanRegeling_documenttype = 'act'"/>
         <xsl:otherwise>
      {"code": "STOP2063", "Work-id": "<xsl:text/>
            <xsl:value-of select="$workVanRegeling"/>
            <xsl:text/>", "melding": "De ExpressionIdentificatie bevat een isTijdelijkdeelVan:WorkIdentificatie:soortWork met '/join/id/stop/work_019' (regeling), maar het derde deel van isTijdelijkdeelVan:WorkIdentificatie:FRBRWork('<xsl:text/>
            <xsl:value-of select="$workVanRegeling"/>
            <xsl:text/>') is niet gelijk aan '/act/'. Pas FRBRWork aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
</xsl:stylesheet>
