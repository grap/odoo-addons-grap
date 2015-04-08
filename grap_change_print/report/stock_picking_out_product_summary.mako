## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
    <style type="text/css">
        ${css}
    </style>
</head>

<body>
    %for wizard in objects :
        <h1 style="clear:both;">${_(u'Products Summary') }</h1>

        <table class="basic_table" width="100%" style="margin-top: 20px;">
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Description")}</th>
                    <th>${_("Standard Price")}</th>
                    <th>${_("Quantity")}</th>
                    <th>${_("UoM")}</th>
                    <th>${_("Standard Price Total")}</th>
                </tr>
            </thead>
            <tbody>
            %for product_line in wizard.product_line_ids:
                <tr class="line">
                     <td style="text-align:left;">${ product_line.product_id.name }</td>
                    <td>${ product_line.standard_price }</td>
                    <td>${ formatLang(product_line.quantity) }</td>
                    <td>${ product_line.uom_id.name }</td>
                    <td>${ product_line.standard_price_total }</td>
                </tr>
            %endfor
            </tbody>
            <tfoot>
                <tr>
                    <th style="text-align:right;" colspan="4">${_("Standard Price Total")}</th>
                    <td>${ wizard.standard_price_total }</td>
                </tr>
            </tfoot>
        </table>

        <h1 style="clear:both;">${_(u'Delivery Orders') }</h1>
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
            %for picking_line in wizard.picking_line_ids:
                <tr class="line" style="background-color:#ddd">
                    <th colspan="2">${ picking_line.picking_id.partner_id.name}</th>
                    <th colspan="3">${ picking_line.picking_id.name}</th>
                </tr>
                %for move_line in picking_line.picking_id.move_lines:

                <tr class="line">
                    <td style="background-color:${move_line.product_id and move_line.product_id.prepare_categ_id and move_line.product_id.prepare_categ_id.color or ''}"
                        >${move_line.product_id and move_line.product_id.prepare_categ_id and move_line.product_id.prepare_categ_id.code or ''}</td>
                     <td style="text-align:left;">${ move_line.product_id.name }</td>
                    <td>${ formatLang(move_line.product_qty) }</td>
                    <td>&nbsp;</td>
                    <td>${ move_line.product_id.uom_id.name }</td>
                </tr>
                %endfor
            %endfor
        </table>
    %endfor
</body>
</html>
