from django.core.management.base import BaseCommand
from bartapp.graph_utils import build_graph, dijkstra

class Command(BaseCommand):
    help = 'Test the pathfinding functionality'

    def handle(self, *args, **kwargs):
        graph = build_graph()
        path, distance = dijkstra(graph, "1", "2")
        self.stdout.write(f'Path: {path}, Distance: {distance}')