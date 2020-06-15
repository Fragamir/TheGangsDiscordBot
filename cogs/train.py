import discord
from discord.ext import commands
from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
import json
import requests
from main import split_send
from urllib.parse import urlencode


class TrainCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        WDSL = "http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01"
        
        self.stations = {}
        with open("station_crs.txt", "r") as f:
            for line in f:
                self.stations[line.split(":")[0]] = (line.split(":")[1]).replace("\n", "")

        history = HistoryPlugin()
        self.wdsl_client = Client(wsdl=WDSL, plugins=[history])
        header = xsd.Element('{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
                             xsd.ComplexType([
                                 xsd.Element(
                                     '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
                                     xsd.String()),
                             ])
                             )
        self.header_value = header(TokenValue=os.environ.get("NRE_TOKEN"))
 
        self.tfl_api_token = json.loads(os.environ)
        

        self.line_id = {
            "bakerloo": 0,
            "central": 1,
            "circle": 2,
            "district": 3,
            "hammersmith-city": 4,
            "jubilee": 5,
            "metropolitan": 6,
            "northern": 7,
            "piccadilly": 8,
            "victoria": 9,
            "waterloo-city": 10
        }

    def tfl_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params.update(self.tfl_api_token)
        params = urlencode(params)
        # https://api.tfl.gov.uk/line/mode/tube/status
        return requests.get("https://api.tfl.gov.uk/" + endpoint + "?" + params)

    @commands.command("departure", aliases=["departures"])
    async def departure(self, context, station):
        resp = self.wdsl_client.service.GetDepartureBoard(numRows=10, crs=station.upper(),
                                                          _soapheaders=[self.header_value])
        services = resp.trainServices.service
        station_full = ""
        for station_name, crs in self.stations.items():
            if crs == station.upper():
                station_full = station_name
        msg = f"Train depatures at {station_full} ({station.upper()})\n"
        i = 0
        while i < len(services):
            t = services[i]
            msg = msg + f"\n{t.std} to {t.destination.location[0].locationName} - {t.etd}"
            i += 1
        await context.send(msg)

    @commands.command("arrival", aliases=["arrivals"])
    async def arrival(self, context, station):
        resp = self.wdsl_client.service.GetArrivalBoard(numRows=10, crs=station.upper(),
                                                        _soapheaders=[self.header_value])
        services = resp.trainServices.service
        station_full = ""
        for station_name, crs in self.stations.items():
            if crs == station.upper():
                station_full = station_name
        msg = f"Train Arrivals at {station_full} ({station.upper()})\n"
        i = 0
        while i < len(services):
            t = services[i]
            # print(t.__dir__)
            msg = msg + f"\n{t.sta} From {t.origin.location[0].locationName} - {t.eta}"
            if t.delayReason:
                pass
            i += 1
        await context.send(msg)

    @commands.group("tfl", aliases=("Tfl","TFL","TfL"))
    async def tfl(self, context):
        pass

    @tfl.command("status", pass_context=True)
    async def status(self, context, line=None):
        response = self.tfl_request("line/mode/tube/status").json()
        if not line:
            msg = ""
            for n in range(0, 10):
                msg += f'{response[n]["name"]}- {response[n]["lineStatuses"][0]["statusSeverityDescription"]}\n'
            split_send(context, msg)
        else:
            try:
                line = int(line)
            except ValueError:
                line = self.line_id.get(line)
                if not line:
                    await context.send(f"""No tube line found with the name {line}, please pick from:\n"""
                                       + f"""{str(self.line_id.keys()).replace("'", "")}""")
                    return
            await context.send(f'{response[line]["name"]}- {response[line]["lineStatuses"][0]["statusSeverityDescription"]}')


def setup(bot):
    bot.add_cog(TrainCog(bot))
