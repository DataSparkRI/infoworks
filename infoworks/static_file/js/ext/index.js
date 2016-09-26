var chart = new InforChart ([], []);

Ext.require([
    'Ext.container.Viewport',
    'Ext.grid.Panel',
    'Ext.grid.plugin.RowEditing',
    'Ext.layout.container.Border'
]);
Ext.Loader.setConfig({
    disableCaching: false
});
Ext.onReady(function() {
    
    Ext.create('Ext.container.Viewport', {
        extend: 'Ext.panel.Panel',
        xtype: 'layout-border',
        requires: [
            'Ext.layout.container.Border'
        ],
        layout: 'border',
        width: "100%",
        height: 400,

        bodyBorder: false,
        
        defaults: {
            collapsible: true,
            split: true,
            bodyPadding: 10
        },
        items: [
        {
            title: 'Chart',
            region: 'south',
            height: "35%",
            minHeight: 75,
            //maxHeight: 150,
            html: '<div id="container" style="min-width: 300px; height: 100%; margin: 1em"></div>',
            tbar: [{
                xtype:'splitbutton',
                text:'Charts',
                iconCls: null,
                glyph: 61,
                menu:[{
                    text:'Column Chart',
                    listeners:{
                       click: function(){chart.type="column";chart.showChart();}
                    }
                },{
                    text:'Line Chart',
                    listeners:{
                       click: function(){chart.type="line";chart.showChart();}
                    }
                }]
            }]
        },
        {
            title: 'Navigation',
            region:'west',
            floatable: false,
            margin: '5 0 0 0',
            width: "30%",
            minWidth: "30%",
            maxWidth: "40%",
            scrollable: true,
            items: nav
        },
        main
        ]
    });    
});
