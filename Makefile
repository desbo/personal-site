deploy:
	jekyll b
	s3_website push
