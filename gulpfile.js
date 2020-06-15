var gulp = require('gulp');
var jade = require('gulp-jade');
var sass = require('gulp-sass');

function html(){
	return gulp.src('src/jade/**/*.jade')
    	.pipe(jade({
      		pretty: true
    	}))
    	.pipe(gulp.dest('django-app/dist/templates/'))
}

function css(){
	return gulp.src('src/sass/**/*.sass')
	    .pipe(sass({
	      pretty: true
	    }))
	    .pipe(gulp.dest('django-app/dist/static/css/'))
}

exports.default = function() {
  gulp.watch('src/jade/**/*.jade', html);
  gulp.watch('src/sass/**/*.sass', css);
};