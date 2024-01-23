package com.nsk.myProject.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.nsk.myProject.Model.Customer;
import com.nsk.myProject.Model.Order;
import com.nsk.myProject.Repositories.CustomerRepository;
import com.nsk.myProject.Repositories.OrderRepository;

import java.util.Optional;

import java.util.List;

@Service
public class CustomerService {
    @Autowired
    private CustomerRepository customerRepository;

    @Autowired
    private OrderRepository orderRepository;

    public Order createOrder(Order order) {
        Long customerId = order.getCustomer().getId();
        Customer customer = customerRepository.findById(customerId)
            .orElseThrow(() -> new RuntimeException("Customer not found with id " + customerId));

        order.setCustomer(customer);
        return orderRepository.save(order);
    }

    public Customer createCustomer(Customer customer) {
        return customerRepository.save(customer);
    }
    public Optional<Customer> getCustomerById(Long id) {
        return customerRepository.findById(id);
    }

    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    public Customer updateCustomer(Long id, Customer customerDetails) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer not found with id " + id));

        customer.setName(customerDetails.getName());
        customer.setEmail(customerDetails.getEmail());

        return customerRepository.save(customer);
    }

    public void deleteCustomer(Long id) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer not found with id " + id));
        
        customerRepository.delete(customer);
    }
}
