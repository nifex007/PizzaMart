from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from django.urls import reverse, resolve
from customers.models import Customer
from pizza_orders.views import OrderReadOnlyViewSet
from pizza_orders.models import Order
from rest_framework import status
import json


# Create your tests here.

class TestOrderView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()

        self.customer = Customer.objects.create(
            full_name='Sharon Aduni Stone',
            email='aduni@sharon.com',
            address='Oke Oja, Aladesuru St., Ayetoro-Ekiti',
            phone='+239460338272'
        )

        self.order = Order.objects.create(
            customer=self.customer,
            flavour='SALAMI',
            count=2,
            size='LARGE'
        )

        self.sample_order_payload = {
            "customer": self.customer.id,
            "flavour": "MARGARITA",
            "size": "SMALL",
            "count": 2
        }

    def test_get_orders(self):
        response = self.client.get(reverse('orders-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_single_order_by_id(self):
        response = self.client.get(reverse('order-detail', args=[self.order.id]))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_single_order_by_id_NOT_FOUND(self):
        response = self.client.get(reverse('order-detail', args=[1000]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_order(self):
        response = self.client.post(reverse('order-list'),

                                    data=json.dumps(self.sample_order_payload),
                                    content_type='application/json'
                                    )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['flavour'], self.sample_order_payload['flavour'])

    def test_edit_order(self):
        payload = {
            "flavour": "MARGARITA",
            "size": "SMALL",
            "count": 5,
            "order_status": "TRANSIT"
        }
        response = self.client.put(reverse('order-detail', args=[self.order.id]),
                                   data=json.dumps(payload),
                                   content_type='application/json'
                                   )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['order_status'], payload['order_status'])
        self.assertEquals(response.data['flavour'], payload['flavour'])
        self.assertEquals(response.data['count'], payload['count'])
        self.assertNotEquals(response.data['order_status'], self.order.order_status)
        self.assertNotEquals(response.data['flavour'], self.order.flavour)
        self.assertNotEquals(response.data['count'], self.order.count)

    def test_partial_edit_order(self):
        payload = {
            "order_status": "TRANSIT"
        }
        response = self.client.patch(reverse('order-detail', args=[self.order.id]),
                                     data=json.dumps(payload),
                                     content_type='application/json'
                                     )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['order_status'], payload['order_status'])
        self.assertNotEquals(response.data['order_status'], self.order.order_status)

    def test_delete_order(self):
        response = self.client.delete(reverse('order-detail', args=[self.order.id]),
                                      content_type='application/json'
                                      )
        check_order = self.client.get(reverse('order-detail', args=[self.order.id]))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(check_order.status_code, status.HTTP_404_NOT_FOUND)

    def test_prevent_edit_of_delivered_order(self):
        # used set order to delivered to match the criteria to be tested
        patch_payload = {
            "order_status": "DELIVERED"
        }
        self.client.patch(reverse('order-detail', args=[self.order.id]),
                          data=json.dumps(patch_payload),
                          content_type='application/json'
                          )
        # test case payload
        put_payload = {
            "flavour": "MARGARITA",
            "size": "SMALL",
            "count": 5,
            "order_status": "TRANSIT"
        }
        response = self.client.put(reverse('order-detail', args=[self.order.id]),
                                   data=json.dumps(put_payload),
                                   content_type='application/json'
                                   )
        expected_message = 'Pizza already delivered to {} at {}'.format(self.order.customer.full_name,
                                                                        self.order.customer.address)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], expected_message)

    def test_prevent_edit_of_in_transit_order(self):
        # used set order to in transit to match the criteria to be tested
        patch_payload = {
            "order_status": "TRANSIT"
        }
        self.client.patch(reverse('order-detail', args=[self.order.id]),
                          data=json.dumps(patch_payload),
                          content_type='application/json'
                          )
        # test case payload
        put_payload = {
            "flavour": "MARGARITA",
            "size": "SMALL",
            "count": 5
        }
        response = self.client.put(reverse('order-detail', args=[self.order.id]),
                                   data=json.dumps(put_payload),
                                   content_type='application/json'
                                   )
        expected_message = 'Pizza already in Transit to {} for {}'.format(self.order.customer.address,
                                                                          self.order.customer.full_name
                                                                          )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], expected_message)

    def test_prevent_partial_edit_of_in_transit_order(self):
        # used set order to in transit to match the criteria to be tested
        patch_payload = {
            "order_status": "TRANSIT"
        }

        self.client.patch(reverse('order-detail', args=[self.order.id]),
                          data=json.dumps(patch_payload),
                          content_type='application/json'
                          )
        # test case payload
        patch_payload = {
            "flavour": "MARGARITA"
        }
        response = self.client.patch(reverse('order-detail', args=[self.order.id]),
                                     data=json.dumps(patch_payload),
                                     content_type='application/json'
                                     )
        expected_message = 'Pizza already in Transit to {} for {}'.format(self.order.customer.address,
                                                                          self.order.customer.full_name
                                                                          )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], expected_message)

    def test_allowing_only_changing_order_status_of_orders_in_transit(self):
        # used set order to in transit to match the criteria to be tested
        patch_payload = {
            "order_status": "TRANSIT"
        }
        self.client.patch(reverse('order-detail', args=[self.order.id]),
                          data=json.dumps(patch_payload),
                          content_type='application/json'
                          )
        # test case payloads
        patch_payload1 = {
            "flavour": "MARGARITA"
        }  # fail

        patch_payload2 = {
            "order_status": "RECIEVED",
            "count": 1
        }  # success | ignores count

        patch_payload3 = {
            "order_status": "DELIVERED",
            "size": "LARGE"
        }  # success | ignores size

        response1 = self.client.patch(reverse('order-detail', args=[self.order.id]),
                                      data=json.dumps(patch_payload1),
                                      content_type='application/json'
                                      )
        expected_message1 = 'Pizza already in Transit to {} for {}'.format(self.order.customer.address,
                                                                           self.order.customer.full_name
                                                                           )

        response2 = self.client.patch(reverse('order-detail', args=[self.order.id]),
                                      data=json.dumps(patch_payload2),
                                      content_type='application/json'
                                      )

        response3 = self.client.patch(reverse('order-detail', args=[self.order.id]),
                                      data=json.dumps(patch_payload3),
                                      content_type='application/json'
                                      )

        self.assertEquals(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response1.data['message'], expected_message1)

        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response2.data['order_status'], 'RECIEVED')
        self.assertEquals(response2.data['count'], self.order.count)

        self.assertEquals(response3.status_code, status.HTTP_200_OK)
        self.assertEquals(response3.data['order_status'], 'DELIVERED')
        self.assertEquals(response3.data['size'], self.order.size)
