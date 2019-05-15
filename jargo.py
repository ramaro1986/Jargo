from lxml import etree
import time

report_file = raw_input("file or path to file: ")
string_compare = raw_input("String to match: ")

try:
	parser = etree.XMLParser(recover=True)
	tree = etree.parse(report_file, parser)
	root = tree.getroot()
	parsed = 'true'
	verify=0

except Exception, inst:
	print "XML ElementTree parsing error opening %s: %s" % (resultFile, inst)
	root = ""
	parsed = 'false'
		

if root.findall('host') is not None:
	host_data_list = root.findall('host')
	
	for host_data in host_data_list:
		hostname_text = ""
		count = 0
		status = host_data.find('status')
		status_text = status.get('state')
		if status_text == "up":
			address = host_data.find("address")
			address_text = address.get('addr')
			hostnames = host_data.find("hostnames")
			hostname_data = hostnames.findall("hostname")
			if hostname_data:
				hostname_text = hostname_data[0].get('name')
			else:
				hostname_text = address_text

			ports = host_data.findall('ports')
			os = host_data.find('os')
			for port in ports:
				port_list = port.findall('port')
				if port_list:
					for port_instance in port_list:
						port_id = port_instance.get('portid')
						#print port_id
						state_display = port_instance.find('state')
						state_of_port = state_display.get('state')

						if  state_of_port == "open":

							oss_version = os.findall('osmatch')
							for os_version in oss_version:
								os_version_text = os_version.get('name')
								break

							service = port_instance.find('service')
							service_name = service.get('name')
							service_product = service.get('product')
							service_version = service.get('version')
							service_os = service.get('ostype')
							try:
								list_results = [service_os, port_id, service_name, service_product, os_version_text]
								if any(string_compare in s for s in list_results):
									if count == 0:
										print "\n%s (%s)." % (address_text,hostname_text)
										count+=1

									print "%s\t%s\t%s\t%s\t%s" % (port_id,service_name,service_product,service_version, os_version_text)
								else:
									pass
							except:
								pass
						else:
							pass
				else:
					pass
			else:
				pass
