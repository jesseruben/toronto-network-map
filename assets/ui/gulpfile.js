var gulp = require('gulp');
var config = require('./gulp.config')();
var $ = require('gulp-load-plugins')({lazy:true});

gulp.task('help', $.taskListing);
gulp.task('default', ['help']);
gulp.task('build', ['scripts', 'templates', 'staticdata','fonts', 'images', 'cssimages', 'minify-rtlcss', 'minify-ltrcss']);

gulp.task('scripts', function() {
    return gulp
        .src(config.alljs)
        .pipe($.concat('app.js'))
        .pipe($.uglify({
            preserveComments: 'some',
            mangle: false,
            compressor: {
                sequences: false,
                hoist_funs: false }
            })
        )
        .pipe(gulp.dest('build/js/'));
});

gulp.task('templates', function() {
   return gulp
        .src(config.templates)
        .pipe(gulp.dest('build/templates/'));
});

gulp.task('staticdata', function() {
   return gulp
        .src(config.staticdata)
        .pipe(gulp.dest('build/staticdata/'));
});

gulp.task('fonts', function() {
   return gulp
       .src(config.fonts)
       .pipe(gulp.dest(config.build + 'fonts'));
});

gulp.task('cssimages', function() {
   return gulp
       .src(config.cssImages)
       .pipe($.imagemin({optimizationLevel: 4}))
       .pipe(gulp.dest(config.build + 'css/images/'));
});

gulp.task('images', function() {
   return gulp
       .src(config.images)
       .pipe($.imagemin({optimizationLevel: 4}))
       .pipe(gulp.dest(config.build + 'img'));
});

gulp.task('minify-rtlcss', function() {
  return gulp.src(config.rtlcss)
    .pipe($.concat('styles.rtl.css'))
    .pipe($.minifyCss())
    .pipe(gulp.dest(config.rtlcssdist));
});

gulp.task('minify-ltrcss', function() {
  return gulp.src(config.ltrcss)
    .pipe($.concat('styles.ltr.css'))
    .pipe($.minifyCss())
    .pipe(gulp.dest(config.ltrcssdist));
});
