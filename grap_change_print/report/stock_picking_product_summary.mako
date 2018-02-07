## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
    <style type="text/css">
        table {
            width:100%;
            margin-top: 20px;
            border-spacing : 0px;
            border-collapse : collapse;
        }
        th {
            border:1px black solid;
        }
        td {
            border:1px black solid;
        }
        
    </style>
</head>

<body>
    %for wizard in objects :
    <!-- Summary Part -->
        %if wizard.print_summary:
        <h1 style="clear:both;">${_(u'Products Summary') }</h1>

        <table>
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Description")}</th>
                    <th>${_("Quantity")}</th>
                    <th>${_("UoM")}</th>
                    <th>${_("Standard Price")}</th>
                    <th>${_("Standard Price Total")}</th>
                </tr>
            </thead>
            <tbody>
            %for product_line in wizard.product_line_ids:
                <tr>
                     <td style="text-align:left;">${ product_line.product_id.name }</td>
                    <td>${ formatLang(product_line.quantity) }</td>
                    <td>${ product_line.uom_id.name }</td>
                    <td>${ product_line.standard_price }</td>
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
        %endif

    <!-- Detail Part -->
        %if wizard.print_detail:
        <h1 style="clear:both;">${_(u'Delivery Orders') }</h1>
        <table>
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

                <tr class="line" style="color:${move_line.product_qty == 0 and 'gray' or 'black'}">
                    <td style="background-color:${move_line.product_id and move_line.product_id.prepare_categ_id and move_line.product_id.prepare_categ_id.color or ''}"
                        >${move_line.product_id and move_line.product_id.prepare_categ_id and move_line.product_id.prepare_categ_id.code or ''}</td>
                     <td style="text-align:left;">${ move_line.product_id.name }</td>
                    <td>${ formatLang(move_line.product_qty) }</td>
                    <td>&nbsp;</td>
                    <td>${ move_line.product_id.uom_id.name }</td>
                </tr>
                %endfor
            %if picking_line.picking_id.note:
                <tr class="line">
                    <td colspan="100%">
                        ${picking_line.picking_id.note}
                    </td>
                </tr>
            %endif
            %endfor
        </table>
        %endif
    %endfor
</body>
</html>
