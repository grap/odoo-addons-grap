## -*- coding: utf-8 -*-
<html>
<head>
<style type="text/css">
${css}
</style>
</head>
<body>
    <h1 style="clear:both;">${_('Products Summary')}</h1>

    %for line in get_product_quantity():
    <br />
    %endfor
    </table>
</body>
</html>
