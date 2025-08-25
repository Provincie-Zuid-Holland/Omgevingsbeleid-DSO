<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
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
      <xsl:apply-templates select="/" mode="M4"/>
      <xsl:apply-templates select="/" mode="M5"/>
      <xsl:apply-templates select="/" mode="M6"/>
      <xsl:apply-templates select="/" mode="M7"/>
      <xsl:apply-templates select="/" mode="M8"/>
      <xsl:apply-templates select="/" mode="M9"/>
      <xsl:apply-templates select="/" mode="M10"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M12"/>
      <xsl:apply-templates select="/" mode="M13"/>
      <xsl:apply-templates select="/" mode="M14"/>
      <xsl:apply-templates select="/" mode="M15"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_data_004OfficieleTitel InformatieObject is JOIN identifier-->
   <!--RULE -->
   <xsl:template match="data:InformatieObjectMetadata" priority="1000" mode="M4">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="starts-with(./data:officieleTitel/string(), '/join/id/')"/>
         <xsl:otherwise> {"code": "STOP1015", "substring": "<xsl:text/>
            <xsl:value-of select="./data:officieleTitel"/>
            <xsl:text/>", "melding": "De waarde van officieleTitel <xsl:text/>
            <xsl:value-of select="./data:officieleTitel"/>
            <xsl:text/> MOET starten met /join/id/. Maak er een JOIN-identifier van.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M4"/>
   <xsl:template match="@*|node()" priority="-2" mode="M4">
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <!--PATTERN sch_data_005Toegestane type informatieobjecten icm publicatie instructie-->
   <!--RULE -->
   <xsl:template match="data:InformatieObjectMetadata" priority="1000" mode="M5">
      <xsl:variable name="formaat"
                    select="normalize-space(xs:string(data:formaatInformatieobject))"/>
      <xsl:variable name="is_GIO"
                    select="$formaat='/join/id/stop/informatieobject/gio_002'"/>
      <xsl:variable name="is_PDF"
                    select="$formaat='/join/id/stop/informatieobject/doc_001'"/>
      <!--REPORT fout-->
      <xsl:if test="$is_GIO and (normalize-space(xs:string(data:publicatieinstructie)) = 'Informatief' or normalize-space(xs:string(data:publicatieinstructie)) = 'AlleenBekendTeMaken') ">
        {"code": "STOP1073", "officieleTitel": "<xsl:text/>
         <xsl:value-of select="data:officieleTitel"/>
         <xsl:text/>", "formaat": "<xsl:text/>
         <xsl:value-of select="$formaat"/>
         <xsl:text/>", "type": "<xsl:text/>
         <xsl:value-of select="data:publicatieinstructie"/>
         <xsl:text/>", "melding": "Een informatieobject <xsl:text/>
         <xsl:value-of select="data:officieleTitel"/>
         <xsl:text/> met formaat <xsl:text/>
         <xsl:value-of select="$formaat"/>
         <xsl:text/> en publicatieinstructie <xsl:text/>
         <xsl:value-of select="data:publicatieinstructie"/>
         <xsl:text/> is niet toegestaan, hiervoor ontbreekt een TPOD instructie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="$is_PDF and normalize-space(xs:string(data:publicatieinstructie)) = 'Informatief' ">
        {"code": "STOP1074", "officieleTitel": "<xsl:text/>
         <xsl:value-of select="data:officieleTitel"/>
         <xsl:text/>", "formaat": "<xsl:text/>
         <xsl:value-of select="$formaat"/>
         <xsl:text/>", "type": "<xsl:text/>
         <xsl:value-of select="data:publicatieinstructie"/>
         <xsl:text/>", "melding": "Een informatieobject <xsl:text/>
         <xsl:value-of select="data:officieleTitel"/>
         <xsl:text/> met formaat <xsl:text/>
         <xsl:value-of select="$formaat"/>
         <xsl:text/> en publicatieinstructie <xsl:text/>
         <xsl:value-of select="data:publicatieinstructie"/>
         <xsl:text/> is niet toegestaan, hiervoor ontbreekt een TPOD instructie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M5"/>
   <xsl:template match="@*|node()" priority="-2" mode="M5">
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <!--PATTERN sch_data_006RegelingVersieMetadata validaties-->
   <!--RULE -->
   <xsl:template match="data:RegelingVersieMetadata/data:versienummer"
                 priority="1000"
                 mode="M6">

		<!--REPORT fout-->
      <xsl:if test="not(matches(./string(), '^[a-zA-Z0-9\-]{1,32}$'))"> {"code": "STOP1016", "substring": "<xsl:text/>
         <xsl:value-of select="./string()"/>
         <xsl:text/>", "melding": "Het versienummer van een regeling <xsl:text/>
         <xsl:value-of select="./string()"/>
         <xsl:text/> MOET bestaan uit maximaal 32 cijfers, onderkast- en bovenkast-letters en -, en MAG NIET bestaan uit punt en underscore.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_data_007informatieobjectRefs uniek-->
   <!--RULE -->
   <xsl:template match="data:informatieobjectRefs" priority="1000" mode="M7">

		<!--REPORT fout-->
      <xsl:if test="count(./data:informatieobjectRef) != count(distinct-values(./data:informatieobjectRef))"> {"code": "STOP1018", "melding": "Alle referenties binnen informatieobjectRefs moeten uniek zijn. Pas dit aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_data_008data:rechtsgebieden, data:overheidsdomeinen, data:onderwerpen,
      data:alternatieveTitels, data:opvolging uniek-->
   <!--RULE -->
   <xsl:template match="data:rechtsgebieden" priority="1004" mode="M8">

		<!--REPORT fout-->
      <xsl:if test="count(./data:rechtsgebied) != count(distinct-values(./data:rechtsgebied))"> {"code": "STOP1019", "melding": "Gebruik elke waarde binnen container data:rechtsgebieden maar één keer.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="data:overheidsdomeinen" priority="1003" mode="M8">

		<!--REPORT fout-->
      <xsl:if test="count(./data:overheidsdomein) != count(distinct-values(./data:overheidsdomein))">
        {"code": "STOP1030", "melding": "Gebruik elke waarde binnen container data:overheidsdomeinen maar één keer.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="data:onderwerpen" priority="1002" mode="M8">

		<!--REPORT fout-->
      <xsl:if test="count(./data:onderwerp) != count(distinct-values(./data:onderwerp))"> {"code": "STOP1031", "melding": "Gebruik elke waarde binnen container data:onderwerpen maar één keer.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="data:alternatieveTitels" priority="1001" mode="M8">

		<!--REPORT fout-->
      <xsl:if test="count(./data:alternatieveTitel) != count(distinct-values(./data:alternatieveTitel))">
        {"code": "STOP1022", "melding": "De alternatieve titels binnen alternatieveTitels MOETEN allen uniek zijn.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="data:opvolging" priority="1000" mode="M8">

		<!--REPORT fout-->
      <xsl:if test="count(./data:opvolgerVan) != count(distinct-values(./data:opvolgerVan))"> {"code": "STOP1023", "melding": "Alle opvolgerVan binnen een opvolging MOETEN uniek zijn.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_data_009alternatieveTitel niet gelijk aan citeertitel-->
   <!--RULE -->
   <xsl:template match="data:alternatieveTitel" priority="1000" mode="M9">

		<!--REPORT fout-->
      <xsl:if test="./string() = ../../data:heeftCiteertitelInformatie/data:CiteertitelInformatie/data:citeertitel/string()"> {"code": "STOP1020", "melding": "De citeertitel MAG NIET gelijk zijn aan een alternatieve titel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_data_010data:opvolgerVan wijst naar een Work van een Regeling of informatieobject-->
   <!--RULE -->
   <xsl:template match="data:opvolgerVan" priority="1000" mode="M10">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./string(), '^/akn/(nl|aw|cw|sx)/act|^/join/id/regdata/')"/>
         <xsl:otherwise>
        {"code": "STOP1024", "substring": "<xsl:text/>
            <xsl:value-of select="./string()"/>
            <xsl:text/>", "melding": "In opvolgerVan (<xsl:text/>
            <xsl:value-of select="./string()"/>
            <xsl:text/>) wordt niet verwezen naar een work van een Regeling of Informatieobject ('/AKN/act/...' of '/join/id/regdata/...'). Corrigeer de verwijzing opvolgerVan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_data_011data:uri moet corresponderen met data:soortRef-->
   <!--RULE -->
   <xsl:template match="data:TekstReferentie" priority="1000" mode="M11">
      <xsl:variable name="is_akn" select="./data:soortRef/string() = 'AKN'"/>
      <xsl:variable name="is_jci" select="./data:soortRef/string() = 'JCI'"/>
      <xsl:variable name="is_url" select="./data:soortRef/string() = 'URL'"/>
      <xsl:variable name="akn_patroon" select="'^/akn/(nl|aw|cw|sx)/act'"/>
      <xsl:variable name="jci_patroon" select="'^jci'"/>
      <xsl:variable name="url_patroon" select="'^http[s]?://'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($is_akn and matches(./data:uri/string(), $akn_patroon)) or ($is_jci and matches(./data:uri/string(), $jci_patroon)) or ($is_url and matches(./data:uri/string(), $url_patroon))"/>
         <xsl:otherwise> {"code": "STOP1021", "substring": "<xsl:text/>
            <xsl:value-of select="./data:uri/string()"/>
            <xsl:text/>", "melding": "De uri <xsl:text/>
            <xsl:value-of select="./data:uri/string()"/>
            <xsl:text/> MOET corresponderen met de soortRef. Pas deze aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_data_013soortBestuursorgaan gevuld voor decentraal-->
   <xsl:variable name="is_decentraal" select="'gemeente|provincie|waterschap'"/>
   <!--RULE -->
   <xsl:template match="data:RegelingMetadata[data:eindverantwoordelijke[matches(., $is_decentraal)]] | data:BesluitMetadata[data:eindverantwoordelijke[matches(., $is_decentraal)]]"
                 priority="1000"
                 mode="M12">

		<!--REPORT fout-->
      <xsl:if test="not(data:soortBestuursorgaan) or data:soortBestuursorgaan = ''">{"code": "STOP1034", "melding": "soortBestuursorgaan MAG NIET leeg zijn voor gemeente, provincie of waterschap. Vul soortBestuursorgaan in.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_data_014soortBestuursorgaan passend bij eindverantwoordelijke-->
   <!--RULE -->
   <xsl:template match="data:RegelingMetadata | data:BesluitMetadata"
                 priority="1000"
                 mode="M13">
      <xsl:variable name="is_gemeente"
                    select="matches(./data:eindverantwoordelijke, 'gemeente')"/>
      <xsl:variable name="is_waterschap"
                    select="matches(./data:eindverantwoordelijke, 'waterschap')"/>
      <xsl:variable name="is_provincie"
                    select="matches(./data:eindverantwoordelijke, 'provincie')"/>
      <xsl:variable name="is_staat"
                    select="matches(./data:eindverantwoordelijke, 'ministerie')"/>
      <xsl:variable name="gemeente_bestuursorgaan_patroon"
                    select="'c_2c4e7407|c_28ecfd6d|c_2a7d8663|^$'"/>
      <xsl:variable name="waterschap_bestuursorgaan_patroon"
                    select="'c_70c87e3d|c_5cc92c89|c_f70a6113|^$'"/>
      <xsl:variable name="provincie_bestuursorgaan_patroon"
                    select="'c_e24d39f6|c_61676cbc|c_411b4e4a|^$'"/>
      <xsl:variable name="staat_bestuursorgaan_patroon"
                    select="'c_bcfb7b4e|c_91fb5e42|c_3aaa4d12|^$'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($is_gemeente and matches(./data:soortBestuursorgaan, $gemeente_bestuursorgaan_patroon)) or ($is_waterschap and matches(./data:soortBestuursorgaan, $waterschap_bestuursorgaan_patroon)) or ($is_provincie and matches(./data:soortBestuursorgaan, $provincie_bestuursorgaan_patroon)) or ($is_staat and matches(./data:soortBestuursorgaan, $staat_bestuursorgaan_patroon)) or (not(./data:eindverantwoordelijke))"/>
         <xsl:otherwise>{"code": "STOP1035", "melding": "soortBestuursorgaan MOET corresponderen met eindverantwoordelijke. Pas soortBestuursorgaan of eindverantwoordelijke aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_data_015-->
   <!--RULE -->
   <xsl:template match="*:heeftGeboorteregeling" priority="1000" mode="M14">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="starts-with(./normalize-space(), '/akn/nl/act')"/>
         <xsl:otherwise>
        {"code": "STOP1060", "Work": "<xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>", "melding": "heeftGeboorteregeling verwijst naar <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>. Dit is geen work van een Regeling ('/AKN/nl/act/...'). Corrigeer de verwijzing heeftGeboorteregeling.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_data_2082-->
   <!--RULE -->
   <xsl:template match="data:soortRegeling" priority="1000" mode="M15">
      <xsl:variable name="voorbeschermingsregels"
                    select="'^/join/id/stop/regelingtype_009$'"/>
      <!--REPORT ontraden-->
      <xsl:if test="matches(./string(),$voorbeschermingsregels)">
        {"code": "STOP2082", "soortRegeling": "<xsl:text/>
         <xsl:value-of select="."/>
         <xsl:text/>", "melding": "Gebruik van de waarde <xsl:text/>
         <xsl:value-of select="."/>
         <xsl:text/> voor soortRegeling wordt ontraden. Gebruik de specifiekere waarden \"Voorbeschermingsregels Omgevingsplan\" of \"Voorbeschermingsregels Omgevingsverordening\".", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
</xsl:stylesheet>
