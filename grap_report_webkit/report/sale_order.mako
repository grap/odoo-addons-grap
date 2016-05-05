## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">

h1{
    padding-top: 26pt;
    font-size: 26pt;
}


        ${css}

td{
    border: 1px solid;
}

.partner_name{
    font-weight: bold;
    font-size: 13px;
}

.partner_address_header{
    font-weight: bold;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>

    <%def name="address(partner)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        %if partner.parent_id:
            <tr><td class="partner_name">${partner.parent_id.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="partner_name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for order in objects:
    <%
      quotation = order.state in ['draft', 'sent']
    %>

    <h1>${quotation and _(u'Devis ') or _(u'Commande de Vente ') } ${order.name}</h1>


    <table>
        <tr>
            <td style="width:33%">
                <table>
                  ${address(partner=order.partner_id)}
                </table>
            </td>
            <td style="width:33%">
                <table>
                    <tr>
                        <td class="partner_address_header">${_("Adresse de livraison")}</td>
                    </tr>
                    ${address(partner=order.partner_shipping_id)}
                </table>
            </td>
            <td style="width:33%">
                <table>
                    <tr>
                        <td class="partner_address_header">${_("Adresse de facturation")}</td>
                    </tr>
                    ${address(partner=order.partner_invoice_id)}
                </table>
            </td>
        </tr>
    </table>

    <table class="basic_table" width="100%">
        <tr>
            <th>${quotation and _("Date de la commande") or _("Date du devis")}</td>
            <th>${_("Vos références")}</td>
            <th>${_("Tarification")}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(order.date_order, date=True)}</td>
            <td>${order.client_order_ref or ''}</td>
            <td>${order.pricelist_id.report_text or ''}</td>
        </tr>
    </table>

    <table class="list_main_table" width="100%">
      <thead>
          <tr>
            <th class="main_col1">${_("Description")}</th>
            <th class="amount main_col2">${_("Qté")}</th>
            <th class="amount main_col3">${_("UdM")}</th>
            <th class="amount main_col4">${_("Price Unitaire")}</th>
            <th class="main_col5">${_("VAT")} ${order.vat_text or ''}</th>
            %if order.has_discount:
            <th class="amount main_col6">${_("Remise (%)")}</th>
            %endif
            <th class="amount main_col7">${_("Sous Total")}</th>
          </tr>
      </thead>
      <tbody>
        %for line in order.order_line:
          <tr>
            <td class="align_top">
                <div class="nobreak">${line.name.replace('\n','<br/>') or '' | n}</div>
            </td>
            <td class="amount main_col2 align_top">${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty) }</td>
            <td class="amount main_col3 align_top">${ line.product_uos and line.product_uos.name or line.product_uom.name }</td>
            <td class="amount main_col4 align_top">${formatLang(line.price_unit)}</td>
            <td class="main_col5 align_top">${ ', '.join([tax.description or tax.name for tax in line.tax_id]) }</td>
            %if order.has_discount:
            <td class="amount main_col6 align_top">${line.discount and formatLang(line.discount, digits=get_digits(dp='Sale Price')) or ''} ${line.discount and '%' or ''}</td>
            %endif
            <td class="amount main_col7 align_top">${formatLang(line.price_subtotal, digits=get_digits(dp='Sale Price'))}&nbsp;${order.pricelist_id.currency_id.symbol}</td>
          </tr>
        %endfor
      </tbody>
      <tfoot class="totals">
        <tr>
          <td colspan="4" class="total_empty_cell"/>
          <td style="font-weight:bold">
            ${_("Net Total:")}
          </td>
          <td class="amount total_sum_cell">
            ${formatLang(order.amount_untaxed, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}
          </td>
        </tr>
        <tr>
          <td colspan="4" class="total_empty_cell"/>
          <td style="font-weight:bold">
            ${_("Taxes:")}
          </td>
          <td class="amount total_sum_cell">
            ${formatLang(order.amount_tax, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}
          </td>
        </tr>
        <tr>
          <td colspan="4" class="total_empty_cell"/>
          <td style="font-weight:bold">
            ${_("Total:")}
          </td>
          <td class="amount total_sum_cell">
            <b>${formatLang(order.amount_total, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}</b>
          </td>
        </tr>
      </tfoot>
    </table>

    %if order.note :
        <p class="std_text">${order.note | carriage_returns}</p>
    %endif
<!--    <p style="page-break-after:always"/>-->
    %endfor
</body>
</html>
