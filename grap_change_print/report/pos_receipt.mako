## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            body{
                font-family: arial, verdana, sans-serif;
                margin:10px;
                font-size:medium;
            }
            table{
                margin-top:10px;
                margin-bottom:10px;
                width:100%;
                border-collapse:collapse;
            }
            table.company_information td{
                text-align:center;
            }
            span.company{
                font-size:x-large;
                font-weight:bold;
            }
            img.company_image{
                margin:0.05cm;
                width:2cm; 
                height:2cm;
            }
            table.sale_information{

            }
            td.sale_information { 
                padding-right:5px;
                text-align:right;
                font-weight:bold;
            }
            table.sale_details{
                margin-top:20px;

            }
            table.sale_details td{
                padding:2px;
            }
        </style>
    </head>
    <body>
    %for pos_order in objects :
        <table class="company_information">
            %if pos_order.company_id.pos_receipt_logo:
            <td>
                <img class="company_image" src="data:image/png;base64,${pos_order.company_id.pos_receipt_logo}"/>
            </td>
            %endif
            <td>
                <span class="company">${pos_order.company_id.name}</span>
                <br />${pos_order.company_id.street}
                %if pos_order.company_id.street2:
                    <br />${pos_order.company_id.street2}
                %endif
                <br />${pos_order.company_id.zip} ${pos_order.company_id.city}
                <br />${pos_order.company_id.phone}
                <br />${pos_order.company_id.email}
                <br />${pos_order.company_id.website}
            </td>
        </table>
        <hr>
        <table class="sale_information">
            <tr>
                <td class="sale_information">N° TVA : </td>
                <td>${pos_order.company_id.vat}</td>
            </tr>
            <tr>
                <td class="sale_information">SIRET : </td>
                <td>${pos_order.company_id.siret}</td>
            </tr>
        </table>
        <hr>
        <table class="sale_information">
            <tr>
                <td class="sale_information">Date : </td>
                <td>${pos_order.date_order}</td>
            </tr>
            <tr>
                <td class="sale_information">Num&eacute;ro : </td>
                <td>${pos_order.name}</td>
            </tr>
            %if pos_order.partner_id:
            <tr>
                <td class="sale_information">Client : </td>
                <td>${pos_order.partner_id.name}</td>
            </tr>
            %endif
        </table>
        <hr>
        <table class="sale_details">
            <tr>
                <th>Description</th>
                <th>Qté</th>
                <th>Prix</th>
            <tr>
            %for pos_order_line in pos_order.lines :
            <tr>
                <td style="padding-right:5px;">${pos_order_line.product_id.name}</td>
                <td style="padding-right:5px;" style="text-align:right">${pos_order_line.qty}</td>
                <td style="text-align:right">${pos_order_line.price_subtotal_incl}&nbsp;${company.currency_id.symbol}</td>
            <tr>
            %if pos_order_line.discount:
            <tr>
                <td colspan="3" style="font-style:italic;">
                (- ${pos_order_line.discount}&nbsp;% 
                soit - ${pos_order_line.discount*pos_order_line.price_unit*pos_order_line.qty/100}&nbsp;${company.currency_id.symbol})
            <tr>
            %endif
            %endfor <!-- end of pos_order_line loop-->
        </table>
        <hr>
        <table style="text-align:right">
            <tr>
                <th>Taxes</th>
                <td>${pos_order.amount_tax}&nbsp;${company.currency_id.symbol}</td>
            <tr>
            <tr>
                <th>Montant HT</th>
                <td>${pos_order.amount_total - pos_order.amount_tax}&nbsp;${company.currency_id.symbol}</td>
            <tr>
            <tr>
                <th>Montant TTC</th>
                <td>${pos_order.amount_total}&nbsp;${company.currency_id.symbol}</td>
            <tr>
        </table>
        <hr>
        <table>
            <tr>
                <th style="text-align:left">Méthode de paiement</th>
                <th style="text-align:left">Montant</th>
            <tr>
            %for pos_statement_line in pos_order.statement_ids :
            <tr>
                <td>${pos_statement_line.journal_id.name}</td>
                <td>${pos_statement_line.amount}&nbsp;${company.currency_id.symbol}</td>
            <tr>
            %endfor <!-- end of pos_statement loop-->
        <table>
    %endfor <!-- end of pos_order loop-->
    </body>
</html>
