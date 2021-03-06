/*jslint browser: true, unparam: true */

(function (tangelo, $, vg) {
    "use strict";

    if (!($ && $.widget && vg)) {
        $.fn.geodots = tangelo.unavailable({
            plugin: "geodots",
            required: ["JQuery", "JQuery UI", "Vega"]
        });
        return;
    }

    $.widget("tangelo.geodots", {
        options: {
            latitude: null,
            longitude: null,
            size: null,
            color: null,
            data: null
        },

        _missing: {
            latitude: 0,
            longitude: 0,
            size: 20,
            color: 0
        },

        _create: function () {
            var that = this;
            var vegaspec = this.options.vegaspec,
                options;

            vg.parse.spec(vegaspec, function (chart) {
                that.vis = chart;

                // Make a copy of the options passed in, but remove the disabled
                // and create attributes (which can cause trouble at the JQuery
                // level), and the vegaspec option (which is only needed once
                // here).
                options = $.extend(true, {}, that.options);
                delete options.disabled;
                delete options.create;
                delete options.vegaspec;

                that._setOptions(options);
            });
        },

        _setOption: function (key, value) {
            if (key !== "data") {
                this._super(key, tangelo.accessor(value, this._missing[key]));
            } else {
                this._super(key, value);
            }
        },

        _setOptions: function (options) {
            var that = this;

            $.each(options, function (key, value) {
                that._setOption(key, value);
            });

            this._update();
        },

        _update: function () {
            var that = this;

            if (this.options.data) {
                this.options.data.forEach(function (d) {
                    d.latitude = that.options.latitude(d);
                    d.longitude = that.options.longitude(d);
                    d.size = that.options.size(d);
                    d.color = that.options.color(d);
                });

                this.vis({
                    el: that.element.get(0),
                    data: {
                        table: that.options.data,
                        links: []
                    }
                }).update();
            }
        }
    });
}(window.tangelo, window.jQuery, window.vg));
