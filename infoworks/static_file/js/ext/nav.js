function getData(url, params, update){
   update.getStore().loadData([]);
   Ext.Ajax.request({
      url: url,
      timeout: 60000,
      method: 'GET',
      scope: this,
      disableCaching:false,
      params: params,
      success: function(resp) {
         console.log(resp);
         update.getStore().loadData(JSON.parse(resp.responseText).genres, true);
      }
   });
}
/* School Type */
Ext.define('Navigation.model.School_type', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'abbr',  type: 'int', convert: null},
        {name: 'init',   type: 'string'},
        {name: 'short_name', type: 'string'},
        {name: 'long_name', type: 'string'}
    ]
});

Ext.define('Navigation.store.School_type', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.school_type',
    model: 'Navigation.model.School_type',
    storeId: 'school_type',
    
    data: [
        [1, 'E', 'Elementary', 'Elementary School'],
        [2, 'M', 'Middle', 'Middle School'],
        [3, 'H', 'High', 'High School'],
    ]
});
/* End of School Type */

/* School Name */
Ext.define('Navigation.model.School', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'school_code',   type: 'string'},
        {name: 'short_name', type: 'string'},
        {name: 'school_name', type: 'string'}
    ]
});

Ext.define('Navigation.store.School', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.school',
    model: 'Navigation.model.School',
    storeId: 'school',
    
    data: []
});

/* End fo School Name */

Ext.define('Navigation.model.Indicator', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'school_indicator_set__title',   type: 'string'},
        {name: 'title__title', type: 'string'}
    ]
});

Ext.define('Navigation.store.Indicator', {
    extend: 'Ext.data.ArrayStore',

    alias: 'store.indicator',

    model: 'Navigation.model.Indicator',
    
    storeId: 'indicator',
    
    data: []
});

/* School Year */
Ext.define('Navigation.model.School_year', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'school_year__school_year',   type: 'string'},

    ]
});

Ext.define('Navigation.store.School_year', {
    extend: 'Ext.data.ArrayStore',

    alias: 'store.school_year',

    model: 'Navigation.model.School_year',
    
    storeId: 'school_year',
    
    data: []
});


nav = [{
        xtype: 'fieldset',
        title: 'School',

        defaultType: 'textfield',
        defaults: {
            anchor: '100%'
        },
        scrollable: true,
        items: [{
                    xtype: 'combobox',
                    fieldLabel: 'School Type',
                    id: 'school_type',
                    store: {
                        type: 'school_type'
                    },
                    valueField: 'abbr',
                    displayField: 'long_name',
                    typeAhead: true,
                    queryMode: 'local',
                    emptyText: 'Select a school type...',
                    listeners: {
                        select: function(combo, records, eOpts) {
                            console.log(records.data);
                            school = Ext.getCmp('school');
                            indicator = Ext.getCmp('indicator');
                            school_year = Ext.getCmp('school_year');
                            school.setValue(null);
                            getData("/api/school","type="+records.data.init,school)
                            indicator.setValue(null);
                            indicator.getStore().loadData([]);
                            school_year.setValue(null);
                            school_year.getStore().loadData([]);
                        },
                    }
                },
                {
                    xtype: 'combobox',
                    fieldLabel: 'School',
                    id: 'school',
                    store: {
                        type: 'school'
                    },
                    valueField: 'school_code',
                    displayField: 'school_name',
                    typeAhead: true,
                    queryMode: 'local',
                    emptyText: 'Select a school type...',
                    listeners: {
                        select: function(combo, records, eOpts) {
                            console.log(records.data);
                            indicator = Ext.getCmp('indicator');
                            indicator.setValue(null);
                            school = Ext.getCmp('school').getValue();
                            getData("/api/school", "school_code="+school, indicator);
                            school_year = Ext.getCmp('school_year');
                            school_year.setValue(null);
                            school_year.getStore().loadData([]);
                        },
                    }
                },
                {
                    xtype: 'combobox',
                    fieldLabel: 'Indicator',
                    id: 'indicator',
                    store: {
                        type: 'indicator'
                    },
                    valueField: 'id',
                    displayField: 'title__title',
                    typeAhead: true,
                    queryMode: 'local',
                    emptyText: 'Select a indicator...',
                    listeners: {
                        select: function(combo, records, eOpts) {
                            console.log(records.data);
                            //main = Ext.getCmp('main');
                            school_year = Ext.getCmp('school_year');
                            school_year.setValue(null);
                            getData("/api/school_indicator", "indicator_id="+records.data.id, school_year);
                            
                        },
                    }
                }
        ]
    }, {
        xtype: 'fieldset',
        title: 'School Year',
        defaultType: 'textfield',

        defaults: {
            anchor: '100%'
        },
        scrollable: true,
        items: [{
                    xtype: 'combobox',
                    fieldLabel: 'School Year',
                    id: 'school_year',
                    store: {
                        type: 'indicator'
                    },
                    valueField: 'id',
                    displayField: 'school_year__school_year',
                    typeAhead: true,
                    queryMode: 'local',
                    emptyText: 'Select a school year...',
                    listeners: {
                        select: function(combo, records, eOpts) {
                            console.log(records.data);
                            main = Ext.getCmp('main');
                            main.reconfigure(default_main_store(), default_main_column())
                            getData("/api/school_indicator", "schooldataset_id="+records.data.id, main);
                            Ext.getCmp('compare_school_year').enable();
                            Ext.getCmp('compare_school').enable();
                            main.getSelectionModel().deselectAll();
                        },
                    }
                },
        ]
    }];
