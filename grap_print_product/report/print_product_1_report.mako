## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
        <style type="text/css">
            body{
                padding:0px;margin:0px;border:0px;overflow:hidden;
            }
            div{
                padding:0px;margin:0px;border:0px;overflow:hidden;
            }
            .label_container{
                page-break-inside: avoid;
                width:7.0cm; height:4cm; float:left;
                background-color:green;
                border:1px solid;
            }
            .barcode_container{
                background-color:yellow;
                border:1px solid;
                position:absolute;
            }
            .product_barcode{
                position:relative;
            }

            .product_name{
                text-align:center;
                position:relative;
                background-color:blue;
            }
            
        </style>
    </head>
    <body>

    %for wizard in objects:

        <!-- For each row -->
        
        %for i in range(0, wizard.print_type_id.row_qty):
            <!-- For each column -->
            %for j in range(0, wizard.print_type_id.column_qty):
            <div class="barcode_container" style="
                    width:${str(wizard.print_type_id.label_width).replace(',', '.')}mm;
                    height:${str(wizard.print_type_id.label_height).replace(',', '.')}mm;
                    top:${str(wizard.print_type_id.page_margin_top +
                        (i * (wizard.print_type_id.inner_margin_top + wizard.print_type_id.label_height))).replace(',', '.')}mm;
                    left:${str(wizard.print_type_id.page_margin_left +
                        (j * (wizard.print_type_id.inner_margin_left + wizard.print_type_id.label_width))).replace(',', '.')}mm
                ">
                <div class="product_name" 
                    style="
                        font-size: ${str(wizard.print_type_id.product_name_font_size).replace(',', '.')}mm;
                        top: ${str(wizard.print_type_id.product_name_top).replace(',', '.')}mm;
                        left: ${str(wizard.print_type_id.product_name_left).replace(',', '.')}mm;
                        width: ${str(wizard.print_type_id.product_name_width).replace(',', '.')}mm;
                        height: ${str(wizard.print_type_id.product_name_height).replace(',', '.')}mm;
                    ">
                    ${wizard.product_id.name}
                </div>

                <img class="product_barcode" 
                    src="data:image/png;base64,${wizard.product_id.ean13_image}"
                    style="
                        top: ${str(wizard.print_type_id.barcode_top).replace(',', '.')}mm;
                        left: ${str(wizard.print_type_id.barcode_left).replace(',', '.')}mm;
                        width: ${str(wizard.print_type_id.barcode_width).replace(',', '.')}mm;
                        height: ${str(wizard.print_type_id.barcode_height).replace(',', '.')}mm;
                    "/>


            </div>
            %endfor
        %endfor
        


    <div style="display:none">
        <!-- ligne 1 -->
        <div class="barcode_container" style="top:2.3cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:2.3cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:2.3cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <!-- ligne 2 -->
        <div class="barcode_container" style="top:7.7cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:7.7cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:7.7cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <!-- ligne 3 -->
        <div class="barcode_container" style="top:13.1cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:13.1cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:13.1cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <!-- ligne 4 -->
        <div class="barcode_container" style="top:18.5cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:18.5cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:18.5cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <!-- ligne 5 -->
        <div class="barcode_container" style="top:23.9cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:23.9cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:23.9cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <!-- ligne 6 -->
        <div class="barcode_container" style="top:29.3cm;left:1.2cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:29.3cm;left:9.1cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
        <div class="barcode_container" style="top:29.3cm;left:17.0cm;">
            <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
        </div>
    </div>

    %endfor
    </body>
</html>


