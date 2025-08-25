<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="data" uri="https://standaarden.overheid.nl/stop/imop/data/"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validaties van Begripsrelaties</sch:p>
   <sch:pattern id="sch_begripsrelaties_1041">
      <sch:p>combinatie wId - catalogusEndPoint moet uniek zijn.</sch:p>
      <sch:rule context="data:Begripsrelaties">
         <sch:let name="Combinaties">
            <xsl:for-each select="data:Begripsrelatie">
               <xsl:sort select="normalize-space(data:wId)"/>
               <combi>
                  <xsl:value-of select="data:wId/string()"/>
                  <xsl:text>|</xsl:text>
                  <xsl:value-of select="data:catalogusEndPoint/string()"/>
               </combi>
            </xsl:for-each>
         </sch:let>
         <sch:let name="DubbeleCombinaties">
            <xsl:for-each select="$Combinaties/combi">
               <xsl:if test="preceding::combi[1] = .">
                  <dubbel>
                     <xsl:value-of select="concat(substring-before(normalize-space(.),'|'), ' - ', substring-after(normalize-space(.),'|'))"/>
                  </dubbel>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:let name="melding">
            <xsl:for-each select="$DubbeleCombinaties/dubbel">
               <xsl:value-of select="."/>
               <xsl:if test="not(position()=last())">
                  <xsl:text>; </xsl:text>
               </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP1041" test="$melding = ''" role="fout">
        {"code": "STOP1041", "Dubbel": "<sch:value-of select="$melding"/>", "melding": "De module Begriprelaties bevat meerdere keren dezelfde data:wId/data:catalogusEndPoint combinatie in data:Begriprelatie: \"<sch:value-of select="$melding"/>\". Elke combinatie mag maar één keer voorkomen. Verwijder dubbele wId/catalogusEndPoint combinaties.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
</sch:schema>
