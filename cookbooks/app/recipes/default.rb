include_recipe "database::postgresql"
      
postgresql_database node['app']['db']['name'] do 
  connection( :host => 'localhost', :username => 'postgres', :password => node['postgresql']['password']['postgres'] ) 
  action :create 
end
