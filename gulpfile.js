var gulp = require('gulp'),
	sass = require('gulp-sass'),
    cleanCSS = require('gulp-clean-css'),
	babel = require('gulp-babel'),
	plumber = require('gulp-plumber'),
    rename = require('gulp-rename');
    run = require('run-sequence');

var paths = {
    css: './theapp/static/css/',
    cssSrc: './static_src/sass/',
    images: './theapp/static/img/',
    imagesSrc: './static_src/img/',
    js: './theapp/static/js/',
    jsSrc: './static_src/js/',
};


gulp.task('sass', function () {  
    gulp.src(`${paths.cssSrc}*.scss`)
    .pipe(plumber())
    .pipe(sass({
        includePaths: ['sass/**']
    }))
    .pipe(gulp.dest(paths.css))
});


gulp.task('js', function () {
    return gulp.src(`${paths.jsSrc}*.es6.js`)
        .pipe(plumber())
        .pipe(rename(function (opt) {
            opt.basename = opt.basename.replace('.es6', '');
            return opt;
        }))
        .pipe(babel())
        .on('error', function (error) {
            utils.error(error.name + ':');
            utils.debug(error.message);
        })
        .pipe(gulp.dest(paths.js));
});


gulp.task('move-images', () => {
    return gulp.src(`${paths.imagesSrc}**/*`)
        .pipe(gulp.dest(paths.images));
});


gulp.task('watch', function () {
  gulp.watch(`${paths.cssSrc}/**/*.scss`, ['sass']);
  gulp.watch(`${paths.jsSrc}/*.es6.js`, ['js']);
});


gulp.task('deploy', function () {
    run('sass', 'move-images','js')
});

