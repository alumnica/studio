var H5P = H5P || {};

H5P.ThreeSixtyImage = (function ($) {
    /**
     * Constructor function.
     */
    function C(options, id) {
        this.$ = $(this);
        this.id = id;
        this.options = $.extend(true, {}, {
            image: null
        }, options);
    }

    /**
     * Attach function called by H5P framework to insert H5P content into
     * page
     *
     * @param {jQuery} $container
     */
    C.prototype.attach = function ($container) {
        var self = this;

        $container.append('<div id="vrview"></div>' +
            '<script src="https://storage.googleapis.com/vrview/2.0/build/vrview.min.js"></script>');

        setTimeout(function () {
            // Selector '#vrview' finds element with id 'vrview'.
            var vrView = new VRView.Player('#vrview', {
                image: H5P.getPath(self.options.image.path, self.id),
                width: 800,
                height: 600
            });
        }, 1000);
    };

    return C;
})(H5P.jQuery);
