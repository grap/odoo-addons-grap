## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}
        .recipient{
            width:50%;
            border: 1px solid;
        }
        }
    </style>
</head>

<body>
    <%page expression_filter="entity"/>

    %for picking in objects:
        <% setLang(picking.partner_id.lang) %>

        <table class="basic_table" width="50%">
                %if picking.partner_id.parent_id:
                <tr><th>${picking.partner_id.parent_id.name or ''}</th></tr>
                <tr><td>${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n")[1:] %>
                %else:
                <tr><td class="name">${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n") %>
                %endif
                %for part in address_lines:
                    %if part:
                    <tr><td>${part}</td></tr>
                    %endif
                %endfor
        </table>

        <h1 style="clear:both;">${_(u'Delivery Order') } ${picking.name}</h1>
        
        <table class="basic_table" width="100%">
            <tr>
                <th>${_("Origin")}</th>
                <th>${_("Scheduled Date")}</th>
                <th>${_('Weight')}</th>
                <th>${_('Delivery Place')}</th>
            </tr>
            <tr>
                <td>${picking.origin or ''}</td>
                <td>${formatLang(picking.min_date, date_time=True)}</td>
                <td>${picking.weight}</td>
                <td>${picking.moment_id and picking.moment_id.place_id.name or ''}</td>
            </tr>
        </table>
    
        <table class="basic_table" width="100%" style="margin-top: 20px;">
            <thead>
                <tr>
                    <th>${_("Type")}</th>
                    <th style="text-align:left;">${_("Description")}</th>
                    <th>${_("Quantity")}</th>
                    <th style="width:60px;">&nbsp;</td>
                    <th>${_("UoM")}</th>
                </tr>
            </thead>
            <tbody>
            %for line in picking.move_lines:
                <tr class="line">
                    <td style="background-color:${line.product_id and line.product_id.prepare_categ_id and line.product_id.prepare_categ_id.color or ''}"
                        >${line.product_id and line.product_id.prepare_categ_id and line.product_id.prepare_categ_id.code or ''}</td>
                    <td style="text-align:left;">${ line.name }</td>
                    <td>${ formatLang(line.product_qty) }</td>
                    <td>&nbsp;</td>
                    <td>${line.product_uom.name}</td>
                </tr>
            %endfor
        </table>
        
        <br/>
        %if picking.note :
            <p class="std_text">${picking.note.replace('\n', '<br />')}</p>
        %endif

        <p style="page-break-after: always"/>
        <br/>
    %endfor
</body>
</html>
