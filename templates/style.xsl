<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml"
                xmlns:html="http://www.w3.org/1999/xhtml"
                version="1.0">
<xsl:output method="xml" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" /> 

<!-- identity -->
<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
</xsl:template>

<xsl:template match="html:head">
    <head>
        <xsl:for-each select="@*">
            <xsl:attribute name="{name(.)}">
                <xsl:value-of select="." />
            </xsl:attribute>
        </xsl:for-each>
        <xsl:choose>
            <xsl:when test="html:title">
                <title><xsl:value-of select="html:title" /> - simpleblog</title>
            </xsl:when>
            <xsl:otherwise>
                <title>simpleblog</title>
            </xsl:otherwise>
        </xsl:choose>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="generator" content="simpleblog" />
        <xsl:apply-templates select="*[name() != 'title']" />
    </head>
</xsl:template>

<xsl:template match="html:body">
    <body>
        <xsl:for-each select="@*">
            <xsl:attribute name="{name(.)}">
                <xsl:value-of select="." />
            </xsl:attribute>
        </xsl:for-each>
        <xsl:apply-templates select="*" />
    </body>
</xsl:template>

</xsl:stylesheet>
