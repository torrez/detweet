# Detweet

My friend Derek ( http://powazek.com/ ) tweeted about wanting to turn off 
the ability for anyone (EVEN ME!) to retweet anything into his stream. I told
him I’d write him a script if it was exposed in the API. It turns out it is.

So last night I wrote this little Tornado app that runs on Heroku. You’ll have
to know how to deploy on Heroku to get it to work. The script expects three
environment variables to be set: twitter_consumer_key, twitter_consumer_secret,
and cookie_secret. (read [this gist](https://gist.github.com/didip/823887) to 
learn how to create a cookie_secret)

Anyway, it doesn’t work. For some reason Twitter’s API says the user’s ability
to retweet is turned off, but it doesn’t actually do it. <s>I do not know 
why and can’t spend time figuring it out.</s> I am told it actually does 
work, it just takes some time. Feel free to take this code and deploy it 
yourself.

http://detweet.herokuapp.com/