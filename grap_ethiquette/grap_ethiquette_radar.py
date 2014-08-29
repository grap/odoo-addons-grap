# -*- coding: utf-8 -*-    
    
CodeSVG = """
<svg width="210" height="210" xmlns="http://www.w3.org/2000/svg" version="1.1">
    <g>
        <!-- Ethical Value : Social To Organic --> 
        <path fill="#a0a0a0" d="M 105,105 L 105,%(y_social)s L %(x_organic)s,105 Z" id="svg_1"/>
        <!-- Ethical Value : Organic To Packaging --> 
        <path fill="#a0a0a0" d="M 105,105 L %(x_organic)s,105 L 105,%(y_packaging)s Z" id="svg_2"/>
        <!-- Ethical Value : Packaging To Local --> 
        <path fill="#a0a0a0" d="M 105,105 L 105,%(y_packaging)s L %(x_local)s,105 Z" id="svg_3"/>
        <!-- Ethical Value : Local To Social --> 
        <path fill="#a0a0a0" d="M 105,105 L %(x_local)s,105 L 105,%(y_social)s Z" id="svg_4"/>

        <!-- base -->
        <line id="svg_101" y2="105" x2="30" y1="105" x1="180" stroke="#919191" fill="none"/>
        <line id="svg_102" y2="30" x2="105" y1="180" x1="105" stroke="#919191" fill="none"/>

        <!-- Niveau 1 -->
        <line id="svg_11" y2="105" x2="120" y1="90" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_12" y2="90" x2="105" y1="105" x1="90" stroke="#919191" fill="none"/>
        <line id="svg_13" y2="105" x2="90" y1="120" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_14" y2="120" x2="105" y1="105" x1="120" stroke="#919191" fill="none"/>

        <!-- Niveau 2 -->
        <line id="svg_21" y2="105" x2="135" y1="75" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_22" y2="75" x2="105" y1="105" x1="75" stroke="#919191" fill="none"/>
        <line id="svg_23" y2="105" x2="75" y1="135" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_24" y2="135" x2="105" y1="105" x1="135" stroke="#919191" fill="none"/>

        <!-- Niveau 3 -->
        <line id="svg_31" y2="105" x2="150" y1="60" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_32" y2="60" x2="105" y1="105" x1="60" stroke="#919191" fill="none"/>
        <line id="svg_33" y2="105" x2="60" y1="150" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_34" y2="150" x2="105" y1="105" x1="150" stroke="#919191" fill="none"/>

        <!-- Niveau 4 -->
        <line id="svg_41" y2="105" x2="165" y1="45" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_42" y2="45" x2="105" y1="105" x1="45" stroke="#919191" fill="none"/>
        <line id="svg_43" y2="105" x2="45" y1="165" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_44" y2="165" x2="105" y1="105" x1="165" stroke="#919191" fill="none"/>

        <!-- Niveau 5 -->
        <line id="svg_51" y2="105" x2="180" y1="30" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_52" y2="30" x2="105" y1="105" x1="30" stroke="#919191" fill="none"/>
        <line id="svg_53" y2="105" x2="30" y1="180" x1="105" stroke="#919191" fill="none"/>
        <line id="svg_54" y2="180" x2="105" y1="105" x1="180" stroke="#919191" fill="none"/>

        <!-- Texte -->
        <text id="svg_111" text-anchor="middle" font-family="Sans-serif" font-size="15" y="110" x="195">AE</text>
        <text id="svg_112" text-anchor="middle" font-family="Sans-serif" font-size="15" y="25" x="105">équitable</text>
        <text id="svg_113" text-anchor="middle" font-family="Sans-serif" font-size="15" y="110" x="18">local</text>
        <text id="svg_114" text-anchor="middle" font-family="Sans-serif" font-size="15" y="195" x="105">emballage</text>
    </g>
</svg>
""" 
