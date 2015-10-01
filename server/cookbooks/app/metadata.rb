name 			  "app"
maintainer        "Snippet Internet Technology Informatica Ltda"
maintainer_email  "sandro@snippet.com.br"
license           "Apache 2.0"
description       "Creates the application mysql database"
long_description  ""
version           "0.0.1"

%w{ centos redhat fedora ubuntu debian arch gentoo oracle amazon scientific}.each do |os|
  supports os
end