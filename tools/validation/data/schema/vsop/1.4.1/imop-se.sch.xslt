<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
                xmlns:se="http://www.opengis.net/se"
                xmlns:ogc="http://www.opengis.net/ogc"
                xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
                xmlns:gml="http://www.opengis.net/gml/3.2"
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
      <xsl:apply-templates select="/" mode="M28"/>
      <xsl:apply-templates select="/" mode="M29"/>
      <xsl:apply-templates select="/" mode="M30"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_se_001-->
   <!--RULE -->
   <xsl:template match="se:FeatureTypeStyle" priority="1000" mode="M8">

		<!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="not(se:Name)"/>
         <xsl:otherwise>
        {"code": "STOP3100", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>", "melding": "De FeatureTypeStyle bevat een Name <xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>, deze informatie wordt genegeerd.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="not(se:Description)"/>
         <xsl:otherwise>
        {"code": "STOP3101", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Description/se:Title/normalize-space()"/>
            <xsl:text/>", "melding": "De FeatureTypeStyle bevat een Description \"<xsl:text/>
            <xsl:value-of select="./se:Description/se:Title/normalize-space()"/>
            <xsl:text/>\", deze informatie wordt genegeerd.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_se_002-->
   <!--RULE -->
   <xsl:template match="se:FeatureTypeName" priority="1000" mode="M9">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="(string(.) = 'Locatie') or (substring-after(string(.), ':') = 'Locatie')"/>
         <xsl:otherwise>
        {"code": "STOP3102", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "De FeatureTypeStyle:FeatureTypeName is <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, dit moet Locatie zijn. Wijzig de FeatureTypeName in Locatie (evt. met een namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_se_003-->
   <!--RULE -->
   <xsl:template match="se:SemanticTypeIdentifier" priority="1000" mode="M10">
      <xsl:variable name="AllowedValue"
                    select="'^(geometrie|groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(substring-after(./string(), ':'), $AllowedValue)"/>
         <xsl:otherwise>
        {"code": "STOP3103", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "De FeatureTypeStyle:SemanticTypeIdentifier is <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, dit moet geo:geometrie, geo:groepID, geo:kwalitatieveNormwaarde of geo:kwantitatieveNormwaarde zijn (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/). Wijzig de SemanticTypeIdentifier.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_se_004-->
   <!--RULE -->
   <xsl:template match="ogc:Filter" priority="1000" mode="M11">
      <xsl:variable name="SemanticTypeId"
                    select="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
      <xsl:variable name="AllowedValue"
                    select="'^(groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($SemanticTypeId, $AllowedValue)"/>
         <xsl:otherwise>
        {"code": "STOP3114", "ID": "<xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/>", "melding": "Rule heeft een Filter terwijl de SemanticTypeIdentifier <xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/> is. Verwijder het Filter, of wijzig de SemanticTypeIdentifier in geo:groepID, geo:kwalitatieveNormwaarde of geo:kwantitatieveNormwaarde zijn (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_se_005-->
   <!--RULE -->
   <xsl:template match="ogc:PropertyName" priority="1000" mode="M12">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./string() = substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
         <xsl:otherwise>
        {"code": "STOP3115", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "ID2": "<xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/>", "melding": "PropertyName is <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, dit moet overeenkomen met de SemanticTypeIdentifier <xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/> (zonder namepace prefix). Corrigeer de PropertyName van het filter of pas de SemanticTypeIdentifier aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_se_006-->
   <!--RULE -->
   <xsl:template match="ogc:PropertyIsBetween | ogc:PropertyIsNotEqualTo | ogc:PropertyIsLessThan | ogc:PropertyIsGreaterThan | ogc:PropertyIsLessThanOrEqualTo | ogc:PropertyIsGreaterThanOrEqualTo"
                 priority="1000"
                 mode="M13">
      <xsl:variable name="SemanticTypeId"
                    select="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
      <xsl:variable name="AllowedValue" select="'^(kwantitatieveNormwaarde)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($SemanticTypeId, $AllowedValue)"/>
         <xsl:otherwise>
        {"code": "STOP3118", "ID": "<xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/>", "melding": "De SemanticTypeIdentifier is <xsl:text/>
            <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
            <xsl:text/>. De operator in Rule:Filter is alleen toegestaan bij SemanticTypeIdentifier geo:kwantitatieveNormwaarde (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/). Corrigeer de operator of pas de SemanticTypeIdentifier aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_se_007-->
   <!--RULE -->
   <xsl:template match="ogc:And" priority="1000" mode="M14">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./ogc:PropertyIsGreaterThanOrEqualTo and ./ogc:PropertyIsLessThan"/>
         <xsl:otherwise>
        {"code": "STOP3120", "ID": "<xsl:text/>
            <xsl:value-of select="preceding::se:Name"/>
            <xsl:text/>", "melding": "In Rule met Rule:Name <xsl:text/>
            <xsl:value-of select="preceding::se:Name"/>
            <xsl:text/> is de operator in Rule:Filter AND, maar de operanden zijn niet PropertyIsLessThan en PropertyIsGreaterThanOrEqualTo. Corrigeer de And expressie in het filter.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_se_008-->
   <!--RULE -->
   <xsl:template match="se:Rule/se:Description" priority="1000" mode="M15">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="se:Title/normalize-space() != ''"/>
         <xsl:otherwise>
        {"code": "STOP3126", "ID": "<xsl:text/>
            <xsl:value-of select="preceding-sibling::se:Name"/>
            <xsl:text/>", "melding": "In Rule met Rule:Name <xsl:text/>
            <xsl:value-of select="preceding-sibling::se:Name"/>
            <xsl:text/> is de Description:Title leeg, deze moet een tekst bevatten die in de legenda getoond kan worden. Voeg de legenda tekst toe aan de Description:Title.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M15"/>
   </xsl:template>
   <!--PATTERN sch_se_009-->
   <!--RULE -->
   <xsl:template match="se:PointSymbolizer" priority="1000" mode="M16">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not(./se:Graphic/se:Mark/se:Fill/se:GraphicFill)"/>
         <xsl:otherwise>
        {"code": "STOP3135", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>", "melding": "De PointSymbolizer van Rule:Name <xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/> heeft een Mark:Fill:GraphicFill, dit is niet toegestaan. Gebruik SvgParameter.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M16"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M16"/>
   <xsl:template match="@*|node()" priority="-2" mode="M16">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M16"/>
   </xsl:template>
   <!--PATTERN sch_se_010-->
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke']"
                 priority="1007"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^#[0-9a-f]{6}$')"/>
         <xsl:otherwise>
       {"code": "STOP3140", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke\" waarde:<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Vul deze met een valide hexadecimale waarde.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'fill']" priority="1006" mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^#[0-9a-f]{6}$')"/>
         <xsl:otherwise>
       {"code": "STOP3147", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"fill\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Vul deze met een valide hexadecimale waarde.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke-width']"
                 priority="1005"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^[0-9]+(.[0-9])?[0-9]?$')"/>
         <xsl:otherwise>
       {"code": "STOP3141", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke-width\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Vul deze met een positief getal met 0,1 of 2 decimalen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke-dasharray']"
                 priority="1004"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^([0-9]+ ?)*$')"/>
         <xsl:otherwise>
       {"code": "STOP3142", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke-dasharray\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Vul deze met setjes van 2 positief gehele getallen gescheiden door spaties.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke-linecap']"
                 priority="1003"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./string() = 'butt'"/>
         <xsl:otherwise>
       {"code": "STOP3143", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke-linecap\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Wijzig deze in \"butt\".", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke-opacity']"
                 priority="1002"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^0((.[0-9])?[0-9]?)|1((.0)?0?)$')"/>
         <xsl:otherwise>
       {"code": "STOP3144", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke-opacity\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Wijzig deze in een decimaal positief getal tussen 0 en 1 (beide inclusief) met 0,1 of 2 decimalen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'fill-opacity']"
                 priority="1001"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^0((.[0-9])?[0-9]?)|1((.0)?0?)$')"/>
         <xsl:otherwise>
       {"code": "STOP3148", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"fill-opacity\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Wijzig deze in een decimaal positief getal tussen 0 en 1 (beide inclusief) met 0,1 of 2 decimalen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="se:SvgParameter[@name = 'stroke-linejoin']"
                 priority="1000"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./string() = 'round'"/>
         <xsl:otherwise>
       {"code": "STOP3145", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "SvgParameter name=\"stroke-linejoin\" waarde: <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>, is ongeldig. Wijzig deze in \"round\".", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M17"/>
   <xsl:template match="@*|node()" priority="-2" mode="M17">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--PATTERN sch_se_011-->
   <!--RULE -->
   <xsl:template match="se:Stroke/se:SvgParameter" priority="1000" mode="M18">
      <xsl:variable name="AllowedValue"
                    select="'^(stroke|stroke-width|stroke-dasharray|stroke-linecap|stroke-opacity|stroke-linejoin)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./@name, $AllowedValue)"/>
         <xsl:otherwise> 
        {"code": "STOP3139", "ID": "<xsl:text/>
            <xsl:value-of select="./@name"/>
            <xsl:text/>", "melding": "Een Stroke:SvgParameter met een ongeldig name attribute <xsl:text/>
            <xsl:value-of select="./@name"/>
            <xsl:text/>. Maak hier een valide name attribute van.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M18"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M18"/>
   <xsl:template match="@*|node()" priority="-2" mode="M18">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M18"/>
   </xsl:template>
   <!--PATTERN sch_se_012-->
   <!--RULE -->
   <xsl:template match="se:Fill/se:SvgParameter" priority="1000" mode="M19">
      <xsl:variable name="AllowedValue" select="'^(fill|fill-opacity)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./@name, $AllowedValue)"/>
         <xsl:otherwise> 
        {"code": "STOP3146", "ID": "<xsl:text/>
            <xsl:value-of select="./@name"/>
            <xsl:text/>", "melding": "Een Fill:SvgParameter met een ongeldig name attribute <xsl:text/>
            <xsl:value-of select="./@name"/>
            <xsl:text/>. Maak hier een valide name-attribute van.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M19"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M19"/>
   <xsl:template match="@*|node()" priority="-2" mode="M19">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M19"/>
   </xsl:template>
   <!--PATTERN sch_se_013-->
   <!--RULE -->
   <xsl:template match="se:WellKnownName" priority="1000" mode="M20">
      <xsl:variable name="AllowedValue"
                    select="'^(cross|cross_fill|square|circle|star|triangle)$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), $AllowedValue)"/>
         <xsl:otherwise>
        {"code": "STOP3157", "ID": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "De Mark:WellKnownName <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/> is niet toegestaan. Maak hier cross(of cross_fill), square, circle, star of triangle van.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M20"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M20"/>
   <xsl:template match="@*|node()" priority="-2" mode="M20">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M20"/>
   </xsl:template>
   <!--PATTERN sch_se_014-->
   <!--RULE -->
   <xsl:template match="se:Size" priority="1000" mode="M21">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^[0-9]+$')"/>
         <xsl:otherwise>
       {"code": "STOP3163", "ID": "<xsl:text/>
            <xsl:value-of select="../../se:Name"/>
            <xsl:text/>", "ID2": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "De (Point/Polygon)symbolizer met se:Name <xsl:text/>
            <xsl:value-of select="../../se:Name"/>
            <xsl:text/> heeft een ongeldige Graphic:Size <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>. Wijzig deze in een geheel positief getal.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M21"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M21"/>
   <xsl:template match="@*|node()" priority="-2" mode="M21">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M21"/>
   </xsl:template>
   <!--PATTERN sch_se_016-->
   <!--RULE -->
   <xsl:template match="se:PolygonSymbolizer/se:Fill/se:GraphicFill/se:Graphic"
                 priority="1000"
                 mode="M22">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./se:ExternalGraphic and not(./se:Mark)"/>
         <xsl:otherwise>
        {"code": "STOP3170", "ID": "<xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/>", "melding": "De PolygonSymbolizer:Fill:GraphicFill:Graphic met Name <xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/> bevat geen se:ExternalGraphic of ook een se:Mark, dit is wel vereist. Voeg een se:ExternalGraphic element toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M22"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M22"/>
   <xsl:template match="@*|node()" priority="-2" mode="M22">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M22"/>
   </xsl:template>
   <!--PATTERN sch_se_017-->
   <!--RULE -->
   <xsl:template match="se:InlineContent[@encoding = 'base64']"
                 priority="1000"
                 mode="M23">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./normalize-space(), '^[A-Z0-9a-z+/ =]*$')"/>
         <xsl:otherwise>
       {"code": "STOP3173", "ID": "<xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/>", "ID2": "<xsl:text/>
            <xsl:value-of select="normalize-space(replace(./string(), '[A-Z0-9a-z+/ =]', ''))"/>
            <xsl:text/>", "melding": "De PolygonSymbolizer:Fill:GraphicFill:Graphic:ExternalGraphic:InlineContent van Rule:Name <xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/> bevat ongeldige tekens <xsl:text/>
            <xsl:value-of select="normalize-space(replace(./string(), '[A-Z0-9a-z+/ =]', ''))"/>
            <xsl:text/>. Wijzig dit. Een base64 encodig mag alleen bestaan uit: hoofd- en kleine letters, cijfers, spaties, plus-teken, /-teken en =-teken.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M23"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M23"/>
   <xsl:template match="@*|node()" priority="-2" mode="M23">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M23"/>
   </xsl:template>
   <!--PATTERN sch_se_018-->
   <!--RULE -->
   <xsl:template match="se:ExternalGraphic/se:Format" priority="1000" mode="M24">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./string() = 'image/png'"/>
         <xsl:otherwise>
       {"code": "STOP3174", "ID": "<xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/>", "ID2": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "De ExternalGraphic:Format van (Polygon)symbolizer:Name <xsl:text/>
            <xsl:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>
            <xsl:text/> heeft een ongeldig Format <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>. Wijzig deze in image/png", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M24"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M24"/>
   <xsl:template match="@*|node()" priority="-2" mode="M24">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M24"/>
   </xsl:template>
   <!--PATTERN sch_se_3176-->
   <!--RULE -->
   <xsl:template match="se:FeatureTypeStyle" priority="1000" mode="M25">
      <xsl:variable name="childnames">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="child::*">
            <xsl:value-of select="node-name(.)"/>
            <xsl:if test="count(following-sibling::*) &gt; 0">, </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(child::*) = 0 or (se:FeatureTypeName and se:SemanticTypeIdentifier and se:Rule)"/>
         <xsl:otherwise>
       {"code": "STOP3176", "childnames": "<xsl:text/>
            <xsl:value-of select="$childnames"/>
            <xsl:text/>", "melding": "FeatureTypeStyle heeft child-elementen: <xsl:text/>
            <xsl:value-of select="$childnames"/>
            <xsl:text/>. Dit is niet correct. FeatureTypeStyle moet FeatureTypeName èn SemanticTypeIdentifier èn een of meer Rule's bevatten OF leeg zijn. Maak de FeatureTypeStyle compleet of verwijder alle child-elementen binnen FeatureTypeStyle.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M25"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M25"/>
   <xsl:template match="@*|node()" priority="-2" mode="M25">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M25"/>
   </xsl:template>
   <!--PATTERN sch_se_3177-->
   <!--RULE -->
   <xsl:template match="se:PointSymbolizer" priority="1000" mode="M26">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not(./se:Graphic/se:ExternalGraphic)"/>
         <xsl:otherwise>
        {"code": "STOP3177", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>", "melding": "De PointSymbolizer:Name <xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/> bevat het element se:ExternalGraphic, dit is niet toegestaan. Pas de PointSymbolizer aan, gebruik se:PointSymbolizer/se:Graphic/se:Mark/se:WellKnownName.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M26"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M26"/>
   <xsl:template match="@*|node()" priority="-2" mode="M26">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M26"/>
   </xsl:template>
   <!--PATTERN sch_se_3178-->
   <!--RULE -->
   <xsl:template match="se:PointSymbolizer" priority="1000" mode="M27">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./se:Graphic/se:Mark/se:Fill"/>
         <xsl:otherwise>
        {"code": "STOP3178", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>", "melding": "De PointSymbolizer:Name <xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/> bevat geen se:Fill, dit is niet toegestaan. Pas de PointSymbolizer aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M27"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M27"/>
   <xsl:template match="@*|node()" priority="-2" mode="M27">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M27"/>
   </xsl:template>
   <!--PATTERN sch_se_3179-->
   <!--RULE -->
   <xsl:template match="se:PointSymbolizer" priority="1000" mode="M28">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="./se:Graphic/se:Mark/se:Stroke"/>
         <xsl:otherwise>
        {"code": "STOP3179", "ID": "<xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/>", "melding": "De PointSymbolizer:Name <xsl:text/>
            <xsl:value-of select="./se:Name"/>
            <xsl:text/> bevat geen se:Stroke, dit is niet toegestaan. Pas de PointSymbolizer aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M28"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M28"/>
   <xsl:template match="@*|node()" priority="-2" mode="M28">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M28"/>
   </xsl:template>
   <!--PATTERN sch_se_3180-->
   <!--RULE -->
   <xsl:template match="se:Rule" priority="1000" mode="M29">
      <xsl:variable name="SemanticTypeId"
                    select="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
      <xsl:variable name="AllowedValue"
                    select="'^(groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
      <!--REPORT fout-->
      <xsl:if test="matches($SemanticTypeId, $AllowedValue) and not(./ogc:Filter)"> 
        {"code": "STOP3180", "ID": "<xsl:text/>
         <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
         <xsl:text/>", "ID2": "<xsl:text/>
         <xsl:value-of select="./se:Name"/>
         <xsl:text/>", "melding": "Rule <xsl:text/>
         <xsl:value-of select="./se:Name"/>
         <xsl:text/> heeft geen Filter terwijl de SemanticTypeIdentifier <xsl:text/>
         <xsl:value-of select="preceding::se:SemanticTypeIdentifier"/>
         <xsl:text/> is. Voeg een Filter toe of wijzig de SemanticTypeIdentifier in geo:geometrie (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M29"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M29"/>
   <xsl:template match="@*|node()" priority="-2" mode="M29">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M29"/>
   </xsl:template>
   <!--PATTERN sch_se_3181-->
   <!--RULE -->
   <xsl:template match="se:PolygonSymbolizer" priority="1000" mode="M30">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="se:Stroke or se:Fill"/>
         <xsl:otherwise>
        {"code": "STOP3181", "ID": "<xsl:text/>
            <xsl:value-of select="se:Name"/>
            <xsl:text/>", "melding": "PolygonSymbolizer <xsl:text/>
            <xsl:value-of select="se:Name"/>
            <xsl:text/> heeft geen Fill of Stroke. Voeg een Fill en/of Stroke toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M30"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M30"/>
   <xsl:template match="@*|node()" priority="-2" mode="M30">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M30"/>
   </xsl:template>
</xsl:stylesheet>
