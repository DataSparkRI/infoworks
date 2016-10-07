var type = 'school';
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
        {name: 'district__district_code', type: 'string'},
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


/* District Name */
Ext.define('Navigation.model.District', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'us_state__state_code', type: 'string'},
        {name: 'district_code',   type: 'string'},
        {name: 'district_name', type: 'string'},
    ]
});

Ext.define('Navigation.store.District', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.district',
    model: 'Navigation.model.District',
    storeId: 'district',
    autoLoad: 'true',
    proxy: {
        type: 'ajax',
        url : '/api/district',
        reader: {type: 'json', root: 'genres'}
    }
});

/* End fo District Name */

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

Ext.define('Navigation.model.DistrictIndicator', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'district_indicator_set__title',   type: 'string'},
        {name: 'title__title', type: 'string'}
    ]
});

Ext.define('Navigation.store.DistrictIndicator', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.district_indicator',
    model: 'Navigation.model.DistrictIndicator',
    storeId: 'district_indicator',
    data: []
});

Ext.define('Navigation.model.StateIndicator', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'state_indicator_set__title',   type: 'string'},
        {name: 'title__title', type: 'string'}
    ]
});

Ext.define('Navigation.store.StateIndicator', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.state_indicator',
    model: 'Navigation.model.StateIndicator',
    storeId: 'state_indicator',
    autoLoad: 'true',
    proxy: {
        type: 'ajax',
        url : '/api/state',
        reader: {type: 'json', root: 'genres'}
    }
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

/* District School Year */
Ext.define('Navigation.model.DistrictSchool_year', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id',  type: 'int', convert: null},
        {name: 'school_year__school_year',   type: 'string'},
    ]
});

Ext.define('Navigation.store.DistrictSchool_year', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.district_school_year',
    model: 'Navigation.model.DistrictSchool_year',
    storeId: 'district_school_year',
    data: []
});

Ext.define('Navigation.store.DistrictSchool_year', {
    extend: 'Ext.data.ArrayStore',
    alias: 'store.state_school_year',
    model: 'Navigation.model.School_year',
    storeId: 'state_school_year',
    data: []
});

school_nav = [{
        xtype: 'fieldset',
        title: 'School',

        defaultType: 'textfield',
        defaults: {
            anchor: '100%'
        },
        scrollable: true,
        items: [{
                    xtype: 'comboboxreset',
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
                        	type = 'school';
                            console.log(records.data);
                            school = Ext.getCmp('school');
                            indicator = Ext.getCmp('indicator');
                            school_year = Ext.getCmp('school_year');
                            school.setValue(null);
                            school_district = Ext.getCmp('school_district').value;
                            if (school_district == null)
                                getData("/api/school","type="+records.data.init,school);
                            else
                            	getData("/api/school","type="+records.data.init+"&district_code="+school_district,school);
                            indicator.setValue(null);
                            indicator.getStore().loadData([]);
                            school_year.setValue(null);
                            school_year.getStore().loadData([]);
                        },
                    }
                },{
                    xtype: 'comboboxreset',
                    fieldLabel: 'District',
                    id: 'school_district',
                    store: {
                        type: 'district'
                    },
                    valueField: 'district_code',
                    displayField: 'district_name',
                    typeAhead: true,
                    queryMode: 'local',
                    emptyText: 'Select a district...',
                    listeners: {
                        select: function(combo, records, eOpts) {
                        	type = 'school';
                            console.log(records.data);
                            school = Ext.getCmp('school');
                            indicator = Ext.getCmp('indicator');
                            school_year = Ext.getCmp('school_year');
                            school.setValue(null);
                            school_type = Ext.getCmp('school_type').value;
                            if (school_type==1)
                            	school_type='E';
                            else if (school_type==2) 
                            	school_type='M';
                            else if (school_type==3)
                                school_type='H';
                            else
                            	school_type=null;
                            if (school_type == null)
                                getData("/api/school","district_code="+records.data.district_code,school);
                            else
                            	getData("/api/school","type="+school_type+"&district_code="+records.data.district_code,school);
                            indicator.setValue(null);
                            indicator.getStore().loadData([]);
                            school_year.setValue(null);
                            school_year.getStore().loadData([]);
                        },
                    }
                },{
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
                        	type = 'school';
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
                },{
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
                        	type = 'school';
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
                        	type = 'school';
                            console.log(records.data);
                            main = Ext.getCmp('main');
                            main.reconfigure(default_main_store('school'), default_main_column('school'));
                            getData("/api/school_indicator", "schooldataset_id="+records.data.id, main);
                            Ext.getCmp('compare_school_year').enable();
                            Ext.getCmp('compare_school').enable();
                            main.getSelectionModel().deselectAll();
                        },
                    }
                },
        ]
    }];



district_nav = [{
    xtype: 'fieldset',
    title: 'District',

    defaultType: 'textfield',
    defaults: {
        anchor: '100%'
    },
    scrollable: true,
    items: [{
                xtype: 'combobox',
                fieldLabel: 'District',
                id: 'district',
                store: {
                    type: 'district'
                },
                valueField: 'district_code',
                displayField: 'district_name',
                typeAhead: true,
                queryMode: 'local',
                emptyText: 'Select a district...',
                listeners: {
                    select: function(combo, records, eOpts) {
                    	type = 'district';
                        console.log(records.data);
                        indicator = Ext.getCmp('district_indicator');
                        indicator.setValue(null);
                        district = Ext.getCmp('district').getValue();
                        getData("/api/district", "district_code="+district, indicator);
                        school_year = Ext.getCmp('school_year');
                        school_year.setValue(null);
                        school_year.getStore().loadData([]);
                    },
                }
            },
            {
                xtype: 'combobox',
                fieldLabel: 'Indicator',
                id: 'district_indicator',
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
                    	type = 'district'
                        console.log(records.data);
                        //main = Ext.getCmp('main');
                        school_year = Ext.getCmp('district_school_year');
                        school_year.setValue(null);
                        getData("/api/district_indicator", "indicator_id="+records.data.id, school_year);
                        
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
                id: 'district_school_year',
                store: {
                    type: 'district_indicator'
                },
                valueField: 'id',
                displayField: 'school_year__school_year',
                typeAhead: true,
                queryMode: 'local',
                emptyText: 'Select a school year...',
                listeners: {
                    select: function(combo, records, eOpts) {
                    	type = 'district';
                        console.log(records.data);
                        main = Ext.getCmp('main');
                        main.reconfigure(default_main_store('district'), default_main_column('district'));
                        getData("/api/district_indicator", "districtdataset_id="+records.data.id, main);
                        Ext.getCmp('compare_school_year').enable();
                        Ext.getCmp('compare_school').enable();
                        main.getSelectionModel().deselectAll();
                    },
                }
            },
    ]
}];

state_nav = [{
    xtype: 'fieldset',
    title: 'State',

    defaultType: 'textfield',
    defaults: {
        anchor: '100%'
    },
    scrollable: true,
    items: [{
                xtype: 'combobox',
                fieldLabel: 'Indicator',
                id: 'state_indicator',
                store: {
                    type: 'state_indicator'
                },
                valueField: 'id',
                displayField: 'title__title',
                typeAhead: true,
                queryMode: 'local',
                emptyText: 'Select a indicator...',
                listeners: {
                    select: function(combo, records, eOpts) {
                    	type = 'state'
                        console.log(records.data);
                        //main = Ext.getCmp('main');
                        school_year = Ext.getCmp('state_school_year');
                        school_year.setValue(null);
                        getData("/api/state_indicator", "indicator_id="+records.data.id, school_year);
                        
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
                id: 'state_school_year',
                store: {
                    type: 'state_indicator'
                },
                valueField: 'id',
                displayField: 'school_year__school_year',
                typeAhead: true,
                queryMode: 'local',
                emptyText: 'Select a school year...',
                listeners: {
                    select: function(combo, records, eOpts) {
                    	type = 'state';
                        console.log(records.data);
                        main = Ext.getCmp('main');
                        main.reconfigure(default_main_store('state'), default_main_column('state'));
                        getData("/api/state_indicator", "statedataset_id="+records.data.id, main);
                        Ext.getCmp('compare_school_year').enable();
                        Ext.getCmp('compare_school').enable();
                        main.getSelectionModel().deselectAll();
                    },
                }
            },
    ]
}];

