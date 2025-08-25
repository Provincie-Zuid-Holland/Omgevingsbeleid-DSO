<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                xmlns:cons="https://standaarden.overheid.nl/stop/imop/consolidatie/"
                xmlns:uws="https://standaarden.overheid.nl/stop/imop/uitwisseling/"
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
      <xsl:apply-templates select="/" mode="M10"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M12"/>
      <xsl:apply-templates select="/" mode="M13"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <xsl:param name="nst" select="'https://standaarden.overheid.nl/stop/imop/tekst/'"/>
   <xsl:param name="nsd" select="'https://standaarden.overheid.nl/stop/imop/data/'"/>
   <xsl:param name="nsg" select="'https://standaarden.overheid.nl/stop/imop/geo/'"/>
   <xsl:param name="nsc"
              select="'https://standaarden.overheid.nl/stop/imop/consolidatie/'"/>
   <!--PATTERN sch_uws_001IMOP-schemaversies in component gelijk-->
   <!--RULE STOP1200-->
   <xsl:template match="uws:Component" priority="1000" mode="M10">
      <xsl:variable name="imop-modules"
                    select="uws:heeftModule/uws:Module[starts-with(uws:namespace,'https://standaarden.overheid.nl/stop/imop/')]"/>
      <xsl:variable name="eersteversie" select="$imop-modules[1]/uws:schemaversie"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="every $v in $imop-modules/uws:schemaversie satisfies $v=$eersteversie"/>
         <xsl:otherwise>
        {"code": "STOP1200", "Work-id": "<xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/>", "melding": "De IMOP-modules binnen de Component met FRBRWork <xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/> hebben niet allemaal dezelfde IMOP-schemaversie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_uws_002een juridische regeltekst MOET samen met een RegelingVersieMetadata-module in component-->
   <xsl:variable name="regelingtypes"
                 select="'RegelingCompact', 'RegelingKlassiek', 'RegelingVrijetekst', 'RegelingTijdelijkdeel'"/>
   <!--RULE STOP1204-->
   <xsl:template match="uws:Component[uws:heeftModule/uws:Module[uws:namespace=$nst][normalize-space(uws:localName)=$regelingtypes]]"
                 priority="1000"
                 mode="M11">

		<!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='RegelingVersieMetadata']"/>
         <xsl:otherwise>
        {"code": "STOP1204", "Work-id": "<xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/>", "melding": "De component <xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/> heeft wel een module met juridische tekst maar geen RegelingVersieMetadata-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_uws_003informatieobject MOET samen met een IO-VersieMetadata-module in component-->
   <xsl:variable name="iotypes"
                 select="'GeoInformatieObjectVaststelling', 'GeoInformatieObjectVersie'"/>
   <!--RULE STOP1205-->
   <xsl:template match="uws:Component [uws:heeftModule/uws:Module[uws:namespace=$nsg][normalize-space(uws:localName)=$iotypes]]"
                 priority="1000"
                 mode="M12">

		<!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='InformatieObjectVersieMetadata']"/>
         <xsl:otherwise>
        {"code": "STOP1205", "Work-id": "<xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/>", "melding": "De component <xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/> heeft wel een module met een informatieobject maar heeft geen InformatieObjectVersieMetadata-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_uws_004Component in een pakbon heeft id-module tenzij soortWork = 024 (versieinformatie) -->
   <!--RULE STOP1208-->
   <xsl:template match="uws:Component" priority="1000" mode="M13">
      <xsl:variable name="SWversieinformatie" select="'/join/id/stop/work_024'"/>
      <xsl:variable name="soortWork"
                    select="descendant::uws:soortWork/normalize-space(string())"/>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="$soortWork=$SWversieinformatie or (uws:heeftModule/uws:Module[uws:namespace=$nsd][normalize-space(uws:localName)='ExpressionIdentificatie']         |uws:heeftModule/uws:Module[uws:namespace=$nsc][normalize-space(uws:localName)='ConsolidatieIdentificatie'])"/>
         <xsl:otherwise>
        {"code": "STOP1208", "Work-id": "<xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/>", "melding": "De Component met <xsl:text/>
            <xsl:value-of select="uws:FRBRWork"/>
            <xsl:text/> heeft geen ExpressionIdentificatie- of ConsolidatieIdentificatie-module. Voeg deze toe aan het uitwisselpakket.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
</xsl:stylesheet>
